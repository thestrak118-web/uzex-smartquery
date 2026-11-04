"""Telegram-bot (aiogram 3)."""
import csv
import html
import io
import logging
import re

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (BotCommand, BufferedInputFile, CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from app.agent import Agent, AllModelsBusy, Answer

log = logging.getLogger("bot")

HELLO = (
    "Assalomu alaykum! Men birja bitimlari bo‘yicha AI-agentman.\n"
    "Savolingizni o‘zbek yoki rus tilida yozing.\n\n"
    "Здравствуйте! Я AI-агент по биржевым сделкам.\n"
    "Задайте вопрос на узбекском или русском языке.\n\n"
    "/new — yangi suhbat / новый диалог\n"
    "/sql — oxirgi SQL / последний SQL"
)
EXAMPLES = [
    "2025-yilda eng ko‘p savdo qilingan 5 ta tovar qaysi?",
    "Qaysi broker eng ko‘p bitim tuzgan?",
    "Какой регион лидирует по объёму торгов в 2025 году?",
    "Средняя цена карбамида в 2024 году",
]

_last: dict[int, Answer] = {}


def to_tg_html(text: str) -> str:
    """Modelning sodda Markdown'ini Telegram HTML ga o'giradi."""
    s = html.escape(text, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", s)
    s = re.sub(r"(?m)^\s*[-*]\s+", "• ", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<i>\1</i>", s)
    return s


def split(text: str, limit: int = 3900) -> list[str]:
    chunks, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > limit and cur:
            chunks.append(cur)
            cur = ""
        cur += line + "\n"
    if cur.strip():
        chunks.append(cur)
    return chunks or [text[:limit]]


def answer_kb(ans: Answer) -> InlineKeyboardMarkup | None:
    row = []
    if ans.sql:
        row.append(InlineKeyboardButton(text="🧾 SQL", callback_data="sql"))
    if ans.table and ans.table.get("rows") and len(ans.table["rows"]) > 1:
        row.append(InlineKeyboardButton(text="📊 CSV", callback_data="csv"))
    return InlineKeyboardMarkup(inline_keyboard=[row]) if row else None


def build_dispatcher(agent: Agent) -> Dispatcher:
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(m: Message):
        agent.reset(f"tg:{m.chat.id}")
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=e, callback_data=f"ex:{i}")] for i, e in enumerate(EXAMPLES)])
        await m.answer(HELLO, reply_markup=kb)

    @dp.message(Command("new", "reset", "yangi"))
    async def new(m: Message):
        agent.reset(f"tg:{m.chat.id}")
        _last.pop(m.chat.id, None)
        await m.answer("Yangi suhbat boshlandi. / Начат новый диалог.")

    @dp.message(Command("sql"))
    async def sql_cmd(m: Message):
        await send_sql(m, m.chat.id)

    async def send_sql(target: Message, chat_id: int):
        ans = _last.get(chat_id)
        if not ans or not ans.sql:
            await target.answer("SQL yo‘q. / SQL нет.")
            return
        body = "\n\n".join(f"<pre>{html.escape(s)}</pre>" for s in ans.sql)
        for chunk in split(body):
            await target.answer(chunk)

    async def handle(m: Message, question: str):
        await m.bot.send_chat_action(m.chat.id, ChatAction.TYPING)
        try:
            ans = await agent.ask(question, session=f"tg:{m.chat.id}")
        except AllModelsBusy as e:
            await m.answer(f"⏳ {e}")
            return
        except Exception as e:
            log.exception("ask failed")
            await m.answer(f"⚠️ AI xizmati xatosi / Ошибка AI-сервиса: {html.escape(str(e))[:500]}")
            return
        _last[m.chat.id] = ans
        chunks = split(to_tg_html(ans.text))
        for i, chunk in enumerate(chunks):
            kb = answer_kb(ans) if i == len(chunks) - 1 else None
            try:
                await m.answer(chunk, reply_markup=kb)
            except Exception:  # HTML buzilgan bo'lsa — oddiy matn
                await m.answer(chunk, parse_mode=None, reply_markup=kb)

    @dp.callback_query(F.data.startswith("ex:"))
    async def example(cb: CallbackQuery):
        q = EXAMPLES[int(cb.data.split(":")[1])]
        await cb.answer()
        await cb.message.answer(f"❓ {html.escape(q)}")
        await handle(cb.message, q)

    @dp.callback_query(F.data == "sql")
    async def sql_cb(cb: CallbackQuery):
        await cb.answer()
        await send_sql(cb.message, cb.message.chat.id)

    @dp.callback_query(F.data == "csv")
    async def csv_cb(cb: CallbackQuery):
        await cb.answer()
        ans = _last.get(cb.message.chat.id)
        if not ans or not ans.table:
            await cb.message.answer("Jadval yo‘q. / Таблицы нет.")
            return
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(ans.table["columns"])
        w.writerows(ans.table["rows"])
        data = ("﻿" + buf.getvalue()).encode("utf-8")  # BOM — Excel uchun
        await cb.message.answer_document(BufferedInputFile(data, filename="natija.csv"))

    @dp.message(F.text)
    async def text(m: Message):
        await handle(m, m.text.strip())

    @dp.message()
    async def other(m: Message):
        await m.answer("Iltimos, savolni matn ko‘rinishida yozing. / Пожалуйста, напишите вопрос текстом.")

    return dp


async def run_bot(agent: Agent, token: str):
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([
        BotCommand(command="start", description="Boshlash / Начать"),
        BotCommand(command="new", description="Yangi suhbat / Новый диалог"),
        BotCommand(command="sql", description="Oxirgi SQL / Последний SQL"),
    ])
    me = await bot.get_me()
    log.info("Telegram-bot ishga tushdi: @%s", me.username)
    await build_dispatcher(agent).start_polling(bot, handle_signals=False)


_webhook: tuple[Bot, Dispatcher] | None = None


async def feed_webhook(agent: Agent, token: str, update: dict):
    """Vercel'dagi /api/telegram/webhook uchun: bitta update'ni qayta ishlaydi."""
    global _webhook
    if _webhook is None:
        _webhook = (Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)), build_dispatcher(agent))
    bot, dp = _webhook
    await dp.feed_webhook_update(bot, update)
