"""Veb-servis: FastAPI + UZEX SmartQuery interfeysi (app/static)."""
import logging
import os
import re
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import db
from app.agent import FALLBACKS, MODEL, Agent, AllModelsBusy, Answer
from app.normalize import detect_lang as detect_lang_full, search_key
from app.sqlfmt import humanize, pretty_sql, top_level_where

log = logging.getLogger("web")
STATIC = Path(__file__).parent / "static"

TABLES = ("deals", "contracts", "companies", "brokers", "usd_rates")
TIME_COLS = re.compile(r"(^|_)(year|month|yil|oy|date|sana|day|period|quarter)s?$", re.I)
NUM_HINT = re.compile(r"(sum|total|amount|count|cnt|deals|volume|price|share|pct|avg|turnover|value|rate|n)$", re.I)


class AskIn(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    language: str | None = Field(default=None, max_length=5)
    conversation_id: str | None = Field(default=None, max_length=64)


class ResetIn(BaseModel):
    conversation_id: str | None = Field(default=None, max_length=64)
    session: str | None = Field(default=None, max_length=64)


def detect_lang(text: str, hint: str | None) -> str:
    lang = detect_lang_full(text)
    if lang:
        return "ru" if lang == "ru" else "uz"
    return hint if hint in ("uz", "ru") else "uz"


def source_of(ans: Answer, lang: str = "uz") -> dict | None:
    if not ans.sql:
        return None
    sql = " ".join(ans.sql)
    tables = [t for t in TABLES if re.search(rf"\b(from|join)\s+{t}\b", sql, re.I)]
    filters, seen = [], set()
    for q in ans.sql:  # faqat asosiy so'rov shartlari, ichki so'rovlarniki emas
        for cond in top_level_where(q):
            f = humanize(cond, lang)
            if f["text"] not in seen:
                seen.add(f["text"])
                filters.append(f)
    return {"tables": tables, "filters": filters[:8], "sql": [pretty_sql(q) for q in ans.sql], "model": ans.model,
            "steps": ans.steps, "seconds": ans.seconds}


def _order_col(sql: str, cols: list[str]) -> int | None:
    """Reyting ko'rsatkichi — SQL dagi ORDER BY ustuni (alias yoki raqam)."""
    m = re.search(r"\border\s+by\s+([\w\"().]+)", sql or "", re.I)
    if not m:
        return None
    key = m.group(1).strip('"').lower()
    if key.isdigit() and 0 < int(key) <= len(cols):
        return int(key) - 1
    low = [c.lower() for c in cols]
    return low.index(key) if key in low else None


VALUE_PRIORITY = re.compile(r"(amount|sum|turnover|uzs|usd|aylanma|summa|oborot|price|narx|volume|tonn|hajm)", re.I)


def visualization_of(ans: Answer, lang: str = "uz") -> dict | None:
    """Natija jadvalidan grafik: bitta yorliq ustuni + bitta son ustuni, 2–30 qator."""
    for t in reversed(ans.tables):
        rows, cols = t.get("rows") or [], t.get("columns") or []
        if not (2 <= len(rows) <= 30) or len(cols) < 2:
            continue
        num = [i for i in range(len(cols)) if all(isinstance(r[i], (int, float)) or r[i] is None for r in rows)]
        text = [i for i in range(len(cols)) if i not in num]
        time_i = next((i for i in range(len(cols)) if TIME_COLS.search(cols[i])), None)
        label_i = time_i if time_i is not None else (text[0] if text else None)
        if label_i is None:
            continue
        if time_i is not None and any(i != label_i for i in text):
            continue  # yil + tovar kabi ikki o'lchovli jadval — bitta qator grafikka sig'maydi
        if time_i is None and lang == "uz":  # o'zbekcha savolga o'zbekcha tovar nomlari
            label_i = next((i for i in text if cols[i].lower().endswith("_uz")), label_i)
        values = [i for i in num if i != label_i and not TIME_COLS.search(cols[i])]
        if not values:
            continue
        order_i = _order_col(t.get("sql", ""), cols)
        val_i = order_i if order_i in values else next(
            (i for pat in (VALUE_PRIORITY, NUM_HINT) for i in values if pat.search(cols[i])), values[0])
        return {
            "type": "line" if time_i is not None and len(rows) > 8 else ("bar" if time_i is not None else "hbar"),
            "title": cols[val_i],
            "label_column": cols[label_i],
            "labels": [str(r[label_i]) for r in rows],
            "values": [r[val_i] for r in rows],
        }
    return None


def create_app(agent: Agent | None = None) -> FastAPI:
    """agent berilmasa, birinchi so'rovda yaratiladi (Vercel: import tez, kalit faqat ish vaqtida kerak)."""
    app = FastAPI(title="UZEX SmartQuery — birja bitimlari AI-agenti", docs_url="/api/docs")
    state = {"agent": agent}

    def get_agent() -> Agent:
        if state["agent"] is None:
            state["agent"] = Agent()
        return state["agent"]

    @app.get("/api/health")
    async def health():
        return {"ok": True, "model": state["agent"].model if state["agent"] else MODEL,
                "models": list(dict.fromkeys([MODEL, *FALLBACKS]))}

    @app.get("/api/v1/stats")
    async def stats():
        con = db.connect()
        by_year = con.execute("""
            select year, count(*), sum(amount_uzs) filter (where not is_cancelled),
                   100.0 * count(*) filter (where is_cancelled) / count(*)
            from deals group by 1 order by 1""").fetchall()
        total, d0, d1 = con.execute("select count(*), min(deal_date), max(deal_date) from deals").fetchone()
        return {
            "deals": total,
            "contracts": con.execute("select count(*) from contracts").fetchone()[0],
            "companies": con.execute("select count(*) from companies").fetchone()[0],
            "brokers": con.execute("select count(*) from brokers").fetchone()[0],
            "first_date": d0.isoformat(), "last_date": d1.isoformat(),
            "by_year": [{"year": y, "deals": n, "turnover_uzs": round(tv), "cancelled_pct": round(c, 2)}
                        for y, n, tv, c in by_year],
            "model": state["agent"].model if state["agent"] else MODEL,
        }

    # ---- UI sahifalari uchun: faqat oldindan yozilgan, parametrli SQL ----
    @app.get("/api/v1/filters")
    async def filters():
        return {
            "years": [r["year"] for r in db.rows("select distinct year from deals order by 1")],
            "products": db.rows("select product, product_uz, count(*) n from deals group by 1, 2 order by 3 desc"),
            "regions": db.rows("select region, region_key, count(*) n from deals group by 1, 2 order by 1"),
            "statuses": db.rows("select status, count(*) n from deals group by 1 order by 2 desc"),
        }

    @app.get("/api/v1/deals")
    async def deals(year: int | None = None, product: str | None = None, region: str | None = None,
                    status: str | None = None, q: str | None = None, page: int = 1, size: int = 25):
        size, page = max(1, min(size, 100)), max(1, page)
        where, params = [], []
        for cond, val in (("d.year = ?", year), ("d.product = ?", product),
                          ("d.region_key = ?", region), ("d.status = ?", status)):
            if val:
                where.append(cond)
                params.append(val)
        q = (q or "").strip()
        if q.isdigit() and len(q) == 9:
            where.append("(d.seller_inn = ? or d.buyer_inn = ?)")
            params += [q, q]
        elif q.isdigit():
            where.append("d.deal_id = ?")
            params.append(int(q))
        elif q:
            key = search_key(q)
            where.append("(d.product_raw ilike ? or s.name_key like ? or b.name_key like ?)")
            params += [f"%{q}%", f"%{key}%", f"%{key}%"]
        base = ("from deals d left join companies s on s.inn = d.seller_inn "
                "left join companies b on b.inn = d.buyer_inn "
                + ("where " + " and ".join(where) if where else ""))
        total = db.rows(f"select count(*) n {base}", params)[0]["n"]
        data = db.rows(f"""
            select d.deal_id, d.deal_date, d.deal_time, d.product, d.product_uz, d.product_spec, d.region,
                   d.volume, d.unit, d.amount, d.currency, d.unit_price, d.start_price, d.status,
                   d.trade_type, d.contract_form, s.name seller, b.name buyer, d.seller_inn, d.buyer_inn
            {base} order by d.deal_id desc limit {size} offset {(page - 1) * size}""", params)
        return {"total": total, "page": page, "size": size, "rows": data}

    @app.get("/api/v1/products")
    async def products(year: int | None = None):
        w, p = ("where year = ?", [year]) if year else ("", [])
        return {"rows": db.rows(f"""
            select product, product_uz, any_value(category) category,
                   string_agg(distinct unit, '/' order by unit) units,
                   count(*) deals, count(*) filter (where is_cancelled) cancelled,
                   sum(amount_uzs) filter (where not is_cancelled) turnover_uzs,
                   sum(volume_tonnes) filter (where not is_cancelled) volume_tonnes,
                   case when count(distinct unit) = 1 then sum(amount_uzs) filter (where not is_cancelled)
                        / sum(volume) filter (where not is_cancelled) end avg_price_uzs,
                   case when count(distinct unit) = 1 then any_value(unit) end price_unit
            from deals {w} group by 1, 2 order by turnover_uzs desc nulls last""", p)}

    @app.get("/api/v1/participants")
    async def participants(role: str = "buyer", year: int | None = None, q: str | None = None, limit: int = 50):
        limit = max(1, min(limit, 200))
        key = search_key(q or "")
        yw, yp = ("and year = ?", [year]) if year else ("", [])
        if role == "broker":
            qw, qp = ("and (br.broker_code = ? or br.name_key like ?)", [(q or "").upper(), f"%{key}%"]) if q else ("", [])
            data = db.rows(f"""
                with b as (select seller_broker code, amount_uzs, is_cancelled, 's' side from deals where true {yw}
                           union all
                           select buyer_broker, amount_uzs, is_cancelled, 'b' from deals where true {yw})
                select br.broker_code id, br.name, br.region, count(*) deals,
                       count(*) filter (where side = 's') seller_side, count(*) filter (where side = 'b') buyer_side,
                       sum(amount_uzs) filter (where not is_cancelled) turnover_uzs
                from b join brokers br on br.broker_code = b.code where true {qw}
                group by all order by deals desc limit {limit}""", yp + yp + qp)
            return {"role": role, "rows": data}
        col = "buyer_inn" if role == "buyer" else "seller_inn"
        qw, qp = ("and (c.inn = ? or c.name_key like ?)", [(q or "").strip(), f"%{key}%"]) if q else ("", [])
        data = db.rows(f"""
            select c.inn id, c.name, c.region, c.activity, count(*) deals,
                   count(distinct d.product) products,
                   sum(d.amount_uzs) filter (where not d.is_cancelled) turnover_uzs
            from deals d join companies c on c.inn = d.{col}
            where true {yw.replace('year', 'd.year')} {qw}
            group by all order by turnover_uzs desc nulls last limit {limit}""", yp + qp)
        return {"role": role, "rows": data}

    @app.get("/api/v1/sources")
    async def sources():
        tables = []
        for t in ("deals", "contracts", "companies", "brokers", "usd_rates"):
            cols = db.rows("select column_name, data_type from information_schema.columns "
                           "where table_name = ? order by ordinal_position", [t])
            n = db.rows(f"select count(*) n from {t}")[0]["n"]
            tables.append({"table": t, "rows": n, "columns": cols})
        norm = db.rows("""select count(distinct product_raw) raw_names, count(distinct product) products,
                                 count(distinct product_spec) specs from contracts""")[0]
        return {"tables": tables, "normalization": norm}

    @app.post("/api/v1/ask")
    async def ask_v1(body: AskIn):
        cid = body.conversation_id or uuid.uuid4().hex[:16]
        lang = detect_lang(body.question, body.language)
        try:
            ans = await get_agent().ask(body.question.strip(), session=f"web:{cid}")
        except AllModelsBusy as e:
            return JSONResponse(status_code=503, content={
                "answer": str(e), "status": "busy", "language": lang, "conversation_id": cid,
                "source": None, "visualization": None, "table": None})
        except Exception as e:
            log.exception("ask failed")
            return JSONResponse(status_code=502, content={
                "answer": f"AI xizmati xatosi / Ошибка AI-сервиса: "
                          f"{e if isinstance(e, RuntimeError) else type(e).__name__}",
                "status": "error", "language": lang, "conversation_id": cid,
                "source": None, "visualization": None, "table": None})
        no_data = bool(ans.sql) and all(not t.get("rows") for t in ans.tables)
        return {
            "answer": ans.text,
            "status": "no_data" if no_data else "ok",
            "language": lang,
            "conversation_id": cid,
            "source": source_of(ans, lang),
            "visualization": visualization_of(ans, lang),
            "table": ans.table,
        }

    @app.post("/api/reset")
    async def reset(body: ResetIn):
        cid = body.conversation_id or body.session
        if cid and state["agent"]:
            state["agent"].reset(f"web:{cid}")
        return {"ok": True}

    # Eski oddiy API (orqaga moslik uchun)
    @app.post("/api/ask")
    async def ask_legacy(body: AskIn):
        try:
            ans = await get_agent().ask(body.question.strip(), session=f"web:{body.conversation_id or 'default'}")
        except AllModelsBusy as e:
            raise HTTPException(503, str(e))
        return {"answer": ans.text, "sql": ans.sql, "table": ans.table,
                "steps": ans.steps, "seconds": ans.seconds, "model": ans.model}

    @app.post("/api/telegram/webhook")
    async def telegram_webhook(request: Request):
        """Serverless (Vercel) uchun: bot polling o'rniga webhook orqali ishlaydi."""
        token, secret = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_WEBHOOK_SECRET")
        if not token or not secret or request.headers.get("X-Telegram-Bot-Api-Secret-Token") != secret:
            raise HTTPException(403)
        from app.bot import feed_webhook
        await feed_webhook(get_agent(), token, await request.json())
        return {"ok": True}

    app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
    return app
