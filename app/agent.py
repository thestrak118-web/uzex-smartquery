"""Gemini asosidagi agent: savol -> (SQL vositalari) -> javob."""
import asyncio
import dataclasses
import datetime as dt
import hashlib
import json
import logging
import os
import re
import time

import httpx
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

from google import genai
from google.genai import errors, types

from app import db, prompt
from app.normalize import LANG_NAMES, detect_lang

log = logging.getLogger("agent")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
# Asosiy model band (503/429) bo'lsa, savol shu modellar bilan qayta ishlanadi
FALLBACKS = [m.strip() for m in os.getenv(
    "GEMINI_FALLBACKS",
    "gemini-3-flash-preview,gemini-3.6-flash,gemini-3.8-flash,gemini-flash-latest,gemini-3.5-flash-lite",
).split(",") if m.strip()]
TRANSIENT = (404, 429, 500, 502, 503, 504)
CALL_TIMEOUT_MS = 25_000  # bitta Gemini chaqiruvi
QUESTION_BUDGET = 70      # bitta savolga jami soniya, keyin «band» xabari
THINKING = os.getenv("GEMINI_THINKING", "").upper()  # MINIMAL / LOW / MEDIUM / HIGH, bo'sh = model standarti
MAX_STEPS = 8
HISTORY_TURNS = 6
CACHE_SALT = "v2-lang-hint"  # agent mantig'i o'zgarsa — eski kesh yaroqsiz


class AllModelsBusy(Exception):
    def __str__(self):
        return ("Gemini limiti vaqtincha tugadi yoki modellar band. Birozdan keyin qayta urinib ko‘ring. / "
                "Лимит Gemini временно исчерпан или модели перегружены. Попробуйте чуть позже.")


def _quota_reset() -> float:
    """Gemini kunlik limiti Tinch okeani vaqti bilan yarim tunda yangilanadi."""
    now = dt.datetime.now(ZoneInfo("America/Los_Angeles"))
    return (now + dt.timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0).timestamp()


def _norm_q(q: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[‘’ʻʼ`']", "'", q.lower())).strip(" ?!.")

TOOLS = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="run_sql",
        description="Run one read-only DuckDB SELECT query over tables deals, contracts, companies, brokers, "
                    "usd_rates. Returns columns, rows (max 60) and whether the result was truncated.",
        parameters_json_schema={
            "type": "object",
            "properties": {"sql": {"type": "string", "description": "A single SELECT / WITH query"}},
            "required": ["sql"],
        },
    ),
    types.FunctionDeclaration(
        name="find_entity",
        description="Fuzzy search of companies and brokers by name (Cyrillic or Latin, partial), 9-digit INN "
                    "(STIR) or broker code like BK012. Returns candidates with inn / broker_code and deal counts.",
        parameters_json_schema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Name, INN or broker code as the user wrote it"},
                "kind": {"type": "string", "enum": ["any", "company", "broker"]},
            },
            "required": ["text"],
        },
    ),
])


@dataclass
class Answer:
    text: str
    sql: list[str] = field(default_factory=list)
    table: dict | None = None  # oxirgi muvaffaqiyatli so'rov natijasi (veb jadval uchun)
    tables: list[dict] = field(default_factory=list)  # barcha muvaffaqiyatli so'rovlar natijalari
    steps: int = 0
    seconds: float = 0.0
    model: str = ""


class Agent:
    def __init__(self, api_key: str | None = None, model: str = MODEL):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY sozlanmagan / не задан (Vercel: Settings → Environment Variables)")
        self.client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=CALL_TIMEOUT_MS))
        self.models = list(dict.fromkeys([model, *FALLBACKS]))
        self.model = model  # oxirgi muvaffaqiyatli model — keyingi savollarda birinchi sinanadi
        self.system = prompt.build()
        self.history: dict[str, list[types.Content]] = {}
        self.cooldown: dict[str, float] = {}  # model -> shu vaqtgacha ishlatilmaydi
        self.cache_ver = hashlib.sha1((CACHE_SALT + self.system).encode()).hexdigest()[:10]
        self.cache_file = db.db_path().with_name("answer_cache.json")
        try:
            self.cache: dict[str, dict] = json.loads(self.cache_file.read_text())
        except (OSError, ValueError):
            self.cache = {}

    def _cache_key(self, q: str) -> str:
        return f"{self.cache_ver}:{_norm_q(q)}"

    def _cache_put(self, q: str, ans: "Answer"):
        self.cache[self._cache_key(q)] = dataclasses.asdict(ans)
        try:
            self.cache_file.write_text(json.dumps(self.cache, ensure_ascii=False))
        except OSError as e:
            log.warning("kesh saqlanmadi: %s", e)

    def _remember(self, session: str, question: str, ans: "Answer"):
        # Tarixga faqat savol va yakuniy javobni saqlaymiz (vosita chaqiruvlarisiz) — tokenlarni tejash uchun
        past = self.history.get(session, [])
        note = f"\n\n[SQL used: {ans.sql[-1]}]" if ans.sql else ""
        turn = [types.Content(role="user", parts=[types.Part.from_text(text=question)]),
                types.Content(role="model", parts=[types.Part.from_text(text=ans.text + note)])]
        self.history[session] = (past + turn)[-HISTORY_TURNS * 2:]

    def reset(self, session: str):
        self.history.pop(session, None)

    def _config(self, tools: bool = True) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=self.system,
            tools=[TOOLS] if tools else None,
            temperature=0.1,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            thinking_config=types.ThinkingConfig(thinking_level=THINKING) if THINKING else None,
        )

    @staticmethod
    def _quota_wait(e: errors.APIError) -> float | None:
        """429 uchun: daqiqalik limit bo'lsa — Google aytgan kutish vaqti, kunlik bo'lsa — None."""
        text = json.dumps(e.details or {}, ensure_ascii=False)
        if "PerDay" in text:
            return None
        m = re.search(r'"retryDelay":\s*"(\d+(?:\.\d+)?)s"', text)
        return min(float(m.group(1)) + 1, 45) if m else 20

    async def _generate(self, model, contents, tools=True):
        # Kutib o'tirmaymiz: band (5xx) bo'lsa bir marta qisqa qayta urinish, 429 — darhol boshqa modelga
        for attempt in range(2):
            try:
                return await self.client.aio.models.generate_content(
                    model=model, contents=contents, config=self._config(tools))
            except errors.APIError as e:
                if attempt == 1 or e.code not in (500, 502, 503, 504):
                    raise
                log.warning("%s: %s, qayta urinish", model, e.code)
                await asyncio.sleep(1.5)

    def _run_tool(self, name: str, args: dict, ans: Answer) -> dict:
        if name == "run_sql":
            sql = args.get("sql", "")
            ans.sql.append(sql)
            res = db.query(sql, max_rows=db.MAX_ROWS_UI)
            if "error" not in res:
                ans.table = res
                ans.tables.append(dict(res, sql=sql))
                llm = dict(res, rows=res["rows"][:db.MAX_ROWS_LLM])
                llm["truncated"] = res["truncated"] or len(res["rows"]) > db.MAX_ROWS_LLM
                return llm
            return res
        if name == "find_entity":
            return db.find_entity(args.get("text", ""), args.get("kind", "any"))
        return {"error": f"unknown tool {name}"}

    async def ask(self, question: str, session: str = "default") -> Answer:
        # Suhbat boshidagi savol keshda bo'lsa — Gemini'ga murojaat qilmaymiz (limitni tejaydi)
        if not self.history.get(session) and (hit := self.cache.get(self._cache_key(question))):
            ans = Answer(**{**hit, "seconds": 0.0})
            self._remember(session, question, ans)
            return ans
        # Model almashsa savol boshidan ishlanadi: Gemini 3 "thought signature"lari boshqa modelga o'tmaydi
        started = time.time()
        for round_ in range(2):
            now = time.time()
            order = [self.model] + [m for m in self.models if m != self.model]
            for model in [m for m in order if self.cooldown.get(m, 0) <= now]:
                if time.time() - started > QUESTION_BUDGET:
                    raise AllModelsBusy()
                try:
                    ans = await self._ask(model, question, session)
                except (httpx.TimeoutException, asyncio.TimeoutError) as e:
                    self.cooldown[model] = time.time() + 30
                    log.warning("%s javob bermadi (%s), keyingi model", model, type(e).__name__)
                    continue
                except errors.APIError as e:
                    if e.code not in TRANSIENT:
                        raise
                    t = time.time()
                    if e.code == 404:
                        self.cooldown[model] = t + 86400
                    elif e.code == 429:
                        wait = self._quota_wait(e)
                        self.cooldown[model] = _quota_reset() if wait is None else t + wait
                    else:
                        self.cooldown[model] = t + 20
                    log.warning("%s ishlamadi (%s), keyingi model", model, e.code)
                    continue
                self.model = model
                if not self.history.get(session) and not ans.text.startswith("Kechirasiz"):
                    self._cache_put(question, ans)
                self._remember(session, question, ans)
                return ans
            # hammasi band: eng tez bo'shaydigan model 30 s ichida bo'shasa — kutib, yana bir aylanamiz
            soon = min(self.cooldown.get(m, 0) for m in self.models) - time.time()
            if round_ or soon > 30 or time.time() - started + soon > QUESTION_BUDGET:
                break
            log.warning("barcha modellar band, %.0fs kutamiz", max(soon, 1))
            await asyncio.sleep(max(soon, 1))
        raise AllModelsBusy()

    async def _ask(self, model: str, question: str, session: str) -> Answer:
        t0 = time.time()
        ans = Answer(text="", model=model)
        past = self.history.get(session, [])
        # Javob tilini serverda aniqlaymiz: model kirillcha o'zbekchani ruschadan ajratishda adashadi
        lang = detect_lang(question)
        hint = f"\n\n[Reply language: {LANG_NAMES[lang]}]" if lang else ""
        contents = past + [types.Content(role="user", parts=[types.Part.from_text(text=question + hint)])]

        for step in range(MAX_STEPS):
            ans.steps = step + 1
            resp = await self._generate(model, contents)
            cand = resp.candidates[0] if resp.candidates else None
            if cand is None or cand.content is None:
                ans.text = "Kechirasiz, javob olinmadi. Savolni qayta yuboring. / Извините, ответ не получен."
                break
            contents.append(cand.content)
            calls = resp.function_calls or []
            if not calls:
                ans.text = (resp.text or "").strip()
                break
            parts = []
            for fc in calls:
                args = dict(fc.args or {})
                log.info("tool %s %s", fc.name, json.dumps(args, ensure_ascii=False)[:500])
                result = await asyncio.to_thread(self._run_tool, fc.name, args, ans)
                parts.append(types.Part.from_function_response(name=fc.name, response={"result": result}))
            contents.append(types.Content(role="user", parts=parts))
        else:
            # qadamlar tugadi — vositasiz yakuniy javob so'raymiz
            contents.append(types.Content(role="user", parts=[types.Part.from_text(
                text="Give the final answer now based on the results above, without more tool calls.")]))
            resp = await self._generate(model, contents, tools=False)
            ans.text = (resp.text or "").strip()

        if not ans.text:
            ans.text = "Kechirasiz, javob tayyorlab bo‘lmadi. / Извините, не удалось подготовить ответ."
        ans.seconds = round(time.time() - t0, 1)
        return ans
