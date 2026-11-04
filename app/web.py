"""Veb-servis: FastAPI + UZEX SmartQuery interfeysi (app/static)."""
import logging
import re
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import db
from app.agent import Agent, AllModelsBusy, Answer

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
    if re.search(r"[ўқғҳЎҚҒҲ]", text):
        return "uz"
    cyr = len(re.findall(r"[А-Яа-яЁё]", text))
    lat = len(re.findall(r"[A-Za-z]", text))
    if cyr > lat:
        return "ru"
    if lat > cyr:
        return "uz"
    return hint if hint in ("uz", "ru") else "uz"


def source_of(ans: Answer) -> dict | None:
    if not ans.sql:
        return None
    sql = " ".join(ans.sql)
    tables = [t for t in TABLES if re.search(rf"\b(from|join)\s+{t}\b", sql, re.I)]
    filters = []
    for q in ans.sql:
        m = re.search(r"\bwhere\b(.+?)(\bgroup\s+by\b|\border\s+by\b|\blimit\b|\bhaving\b|\)\s*select\b|$)",
                      q, re.I | re.S)
        if m:
            f = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(";")
            if f and f not in filters:
                filters.append(f[:300])
    return {"tables": tables, "filters": filters, "sql": ans.sql, "model": ans.model,
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


def create_app(agent: Agent) -> FastAPI:
    app = FastAPI(title="UZEX SmartQuery — birja bitimlari AI-agenti", docs_url="/api/docs")

    @app.get("/api/health")
    async def health():
        return {"ok": True, "model": agent.model}

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
            "model": agent.model,
        }

    @app.post("/api/v1/ask")
    async def ask_v1(body: AskIn):
        cid = body.conversation_id or uuid.uuid4().hex[:16]
        lang = detect_lang(body.question, body.language)
        try:
            ans = await agent.ask(body.question.strip(), session=f"web:{cid}")
        except AllModelsBusy as e:
            return JSONResponse(status_code=503, content={
                "answer": str(e), "status": "busy", "language": lang, "conversation_id": cid,
                "source": None, "visualization": None, "table": None})
        except Exception as e:
            log.exception("ask failed")
            return JSONResponse(status_code=502, content={
                "answer": f"AI xizmati xatosi / Ошибка AI-сервиса: {type(e).__name__}",
                "status": "error", "language": lang, "conversation_id": cid,
                "source": None, "visualization": None, "table": None})
        no_data = bool(ans.sql) and all(not t.get("rows") for t in ans.tables)
        return {
            "answer": ans.text,
            "status": "no_data" if no_data else "ok",
            "language": lang,
            "conversation_id": cid,
            "source": source_of(ans),
            "visualization": visualization_of(ans, lang),
            "table": ans.table,
        }

    @app.post("/api/reset")
    async def reset(body: ResetIn):
        cid = body.conversation_id or body.session
        if cid:
            agent.reset(f"web:{cid}")
        return {"ok": True}

    # Eski oddiy API (orqaga moslik uchun)
    @app.post("/api/ask")
    async def ask_legacy(body: AskIn):
        try:
            ans = await agent.ask(body.question.strip(), session=f"web:{body.conversation_id or 'default'}")
        except AllModelsBusy as e:
            raise HTTPException(503, str(e))
        return {"answer": ans.text, "sql": ans.sql, "table": ans.table,
                "steps": ans.steps, "seconds": ans.seconds, "model": ans.model}

    app.mount("/", StaticFiles(directory=STATIC, html=True), name="static")
    return app
