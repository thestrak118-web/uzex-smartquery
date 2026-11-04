"""DuckDB bilan xavfsiz ishlash: faqat o'qish, fayl tizimiga kirish yopiq, vaqt chegarasi."""
import datetime as dt
import decimal
import logging
import os
import re
import tempfile
import threading
from pathlib import Path

import duckdb

from app.normalize import search_key

log = logging.getLogger("db")
ROOT = Path(__file__).resolve().parent.parent
LOCAL_DB = ROOT / "data" / "uzex.duckdb"
QUERY_TIMEOUT = 20  # soniya
MAX_ROWS_LLM = 60   # LLM ga qaytariladigan qatorlar
MAX_ROWS_UI = 500   # veb jadval uchun

_con: duckdb.DuckDBPyConnection | None = None
_lock = threading.Lock()


def db_path() -> Path:
    """UZEX_DB > data/uzex.duckdb (lokal) > /tmp/uzex.duckdb (Vercel kabi faqat-o'qish muhit)."""
    if os.getenv("UZEX_DB"):
        return Path(os.environ["UZEX_DB"])
    if LOCAL_DB.exists() or (not os.getenv("VERCEL") and os.access(ROOT, os.W_OK)):
        return LOCAL_DB
    return Path(tempfile.gettempdir()) / "uzex.duckdb"


def connect() -> duckdb.DuckDBPyConnection:
    global _con
    with _lock:
        if _con is None:
            path = db_path()
            if not path.exists():  # birinchi ishga tushish: dataset zip'idan bazani quramiz
                import prepare
                log.info("Baza qurilmoqda: %s", path)
                prepare.build(path, verbose=False)
            con = duckdb.connect(str(path), read_only=True)
            con.execute("SET enable_external_access = false")
            con.execute("SET lock_configuration = true")
            _con = con
    return _con


_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|create|drop|alter|attach|detach|copy|export|import|install|load|"
    r"pragma|set|reset|call|checkpoint|vacuum|use)\b",
    re.I,
)


def _strip_comments(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    return re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)


def _check(sql: str) -> str:
    s = _strip_comments(sql).strip().rstrip(";").strip()
    if ";" in s:
        raise ValueError("Faqat bitta SQL so'rov yuborish mumkin")
    if not re.match(r"^(select|with|from|summarize|describe)\b", s, re.I):
        raise ValueError("Faqat SELECT so'rovlariga ruxsat bor")
    # satr literallarini olib tashlab, kalit so'zlarni tekshiramiz
    bare = re.sub(r"'(?:[^']|'')*'", "''", s)
    if m := _FORBIDDEN.search(bare):
        raise ValueError(f"Taqiqlangan operator: {m.group(1)}")
    return s


def _fmt(v):
    if isinstance(v, float):
        return round(v, 4) if abs(v) < 1000 else round(v, 2)
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (dt.date, dt.datetime, dt.time)):
        return v.isoformat()
    return v


def query(sql: str, max_rows: int = MAX_ROWS_UI) -> dict:
    """SQL ni bajaradi. Natija: {columns, rows, row_count, truncated} yoki {error}."""
    try:
        s = _check(sql)
    except ValueError as e:
        return {"error": str(e)}
    cur = connect().cursor()
    timer = threading.Timer(QUERY_TIMEOUT, cur.interrupt)
    timer.start()
    try:
        rel = cur.execute(s)
        columns = [d[0] for d in rel.description] if rel.description else []
        rows = rel.fetchmany(max_rows + 1)
    except duckdb.InterruptException:
        return {"error": f"So'rov {QUERY_TIMEOUT} soniyadan oshdi — soddaroq so'rov yozing"}
    except duckdb.Error as e:
        return {"error": f"{type(e).__name__}: {str(e)[:800]}"}
    finally:
        timer.cancel()
        cur.close()
    truncated = len(rows) > max_rows
    rows = [[_fmt(v) for v in r] for r in rows[:max_rows]]
    return {"columns": columns, "rows": rows, "row_count": len(rows), "truncated": truncated}


def find_entity(text: str, kind: str = "any", limit: int = 10) -> dict:
    """Kompaniya / broker qidirish: nom (kirill yoki lotin), STIR yoki broker kodi bo'yicha."""
    q = text.strip()
    con = connect()
    out = []
    digits = re.sub(r"\D", "", q)
    key = search_key(q)
    if kind in ("any", "company"):
        if len(digits) == 9 and digits == q.replace(" ", ""):
            where, params = "c.inn = ?", [digits]
        else:
            where = "(c.name_key like '%' || ? || '%' or jaro_winkler_similarity(c.name_key, ?) > 0.85)"
            params = [key, key]
        rows = con.execute(f"""
            select 'company' as kind, c.inn, c.name, c.region, c.role, c.activity,
                   (select count(*) from deals d where d.seller_inn = c.inn) as deals_as_seller,
                   (select count(*) from deals d where d.buyer_inn = c.inn) as deals_as_buyer,
                   case when c.inn = ? then 3 when c.name_key = ? then 2
                        when c.name_key like ? || '%' then 1 else 0 end
                     + jaro_winkler_similarity(c.name_key, ?) as score
            from companies c where {where}
            order by score desc limit {limit}""", [digits, key, key, key, *params]).fetchall()
        out += [dict(zip(["kind", "inn", "name", "region", "role", "activity",
                          "deals_as_seller", "deals_as_buyer", "score"], r)) for r in rows]
    if kind in ("any", "broker"):
        code = q.upper().replace(" ", "")
        rows = con.execute(f"""
            select 'broker' as kind, b.broker_code, b.name, b.inn, b.region,
                   (select count(*) from deals d where d.seller_broker = b.broker_code) as deals_seller_side,
                   (select count(*) from deals d where d.buyer_broker = b.broker_code) as deals_buyer_side,
                   case when b.broker_code = ? or b.inn = ? then 3 when b.name_key = ? then 2
                        when b.name_key like ? || '%' then 1 else 0 end
                     + jaro_winkler_similarity(b.name_key, ?) as score
            from brokers b
            where b.broker_code = ? or b.inn = ? or b.name_key like '%' || ? || '%'
               or jaro_winkler_similarity(b.name_key, ?) > 0.85
            order by score desc limit {limit}""",
            [code, digits, key, key, key, code, digits, key, key]).fetchall()
        out += [dict(zip(["kind", "broker_code", "name", "inn", "region",
                          "deals_seller_side", "deals_buyer_side", "score"], r)) for r in rows]
    out.sort(key=lambda r: -r["score"])
    for r in out:
        r["score"] = round(r["score"], 3)
    return {"query_key": key, "matches": out[:limit]}


def rows(sql: str, params: list | None = None) -> list[dict]:
    """Ishonchli (bizning) SQL + parametrlar -> dict qatorlar. UI sahifalari uchun."""
    cur = connect().cursor()
    try:
        rel = cur.execute(sql, params or [])
        cols = [d[0] for d in rel.description]
        return [dict(zip(cols, [_fmt(v) for v in r])) for r in rel.fetchall()]
    finally:
        cur.close()
