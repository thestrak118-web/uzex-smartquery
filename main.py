"""Bitta jarayonda veb-servis va Telegram-botni ishga tushiradi.

    python main.py            # veb + bot (TELEGRAM_BOT_TOKEN bo'lsa)
    python main.py --web      # faqat veb
    python main.py --bot      # faqat bot
    python main.py --ask "2025-yilda nechta bitim bo'lgan?"   # terminalda bitta savol
    python main.py --models   # API kalit bilan mavjud Gemini modellar ro'yxati
"""
import argparse
import asyncio
import logging
import os

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)


async def run(args):
    from app.agent import Agent
    agent = Agent()
    tasks = []
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not args.bot:
        import uvicorn
        from app.web import create_app
        host, port = os.getenv("WEB_HOST", "0.0.0.0"), int(os.getenv("WEB_PORT", "8000"))
        server = uvicorn.Server(uvicorn.Config(create_app(agent), host=host, port=port, log_level="info"))
        logging.info("Veb: http://localhost:%s", port)
        tasks.append(server.serve())
    if not args.web:
        if token:
            from app.bot import run_bot
            tasks.append(run_bot(agent, token))
        elif args.bot:
            raise SystemExit("TELEGRAM_BOT_TOKEN .env faylda yo'q")
        else:
            logging.warning("TELEGRAM_BOT_TOKEN yo'q — faqat veb ishga tushdi")
    await asyncio.gather(*tasks)


async def ask_once(q: str):
    from app.agent import Agent
    ans = await Agent().ask(q)
    print(ans.text)
    print(f"\n--- {ans.model}, {ans.steps} qadam, {ans.seconds} s")
    for s in ans.sql:
        print("SQL:", s)


def list_models():
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    for m in client.models.list():
        if "generateContent" in (m.supported_actions or []):
            print(m.name.removeprefix("models/"))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--web", action="store_true")
    g.add_argument("--bot", action="store_true")
    g.add_argument("--ask")
    g.add_argument("--models", action="store_true")
    a = p.parse_args()
    if a.models:
        list_models()
    elif a.ask:
        asyncio.run(ask_once(a.ask))
    else:
        asyncio.run(run(a))
