"""Agentni test savollar bo'yicha tekshirish: python -m eval.run_eval [--only 1,5,7]"""
import argparse
import asyncio
import re
import sys
import time

from dotenv import load_dotenv

load_dotenv()

from app import db  # noqa: E402
from app.agent import Agent  # noqa: E402
from app.normalize import search_key  # noqa: E402
from eval.cases import CASES  # noqa: E402

MULT = {"ming": 1e3, "тыс": 1e3, "mln": 1e6, "млн": 1e6, "million": 1e6, "миллион": 1e6,
        "mlrd": 1e9, "млрд": 1e9, "milliard": 1e9, "миллиард": 1e9, "trln": 1e12, "трлн": 1e12,
        "trillion": 1e12, "триллион": 1e12}
NUM_RE = re.compile(r"(\d{1,3}(?:[   ]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)\s*([A-Za-zА-Яа-яЁё]+)?")


def numbers(text: str) -> list[float]:
    out = []
    for m in NUM_RE.finditer(text):
        raw = re.sub(r"[   ]", "", m.group(1)).replace(",", ".")
        try:
            v = float(raw)
        except ValueError:
            continue
        out.append(v)
        word = (m.group(2) or "").lower()
        for k, mul in MULT.items():
            if word.startswith(k):
                out.append(v * mul)
    return out


def check(answer: str, expected: list, text: bool) -> bool:
    if text:
        a = search_key(answer)
        return all(search_key(str(e))[:10] in a for e in expected if e is not None)
    got = numbers(answer)
    for e in expected:
        if e is None:
            continue
        e = float(e)
        tol = max(abs(e) * 0.011, 0.051)
        if not any(abs(g - e) <= tol for g in got):
            return False
    return True


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--only", help="1,2,5 — faqat shu raqamli savollar")
    p.add_argument("--pause", type=float, default=0, help="savollar orasida pauza (bepul tarif limiti uchun)")
    args = p.parse_args()
    only = {int(x) for x in args.only.split(",")} if args.only else None
    agent = Agent()
    ok = total = 0
    for i, c in enumerate(CASES, 1):
        if only and i not in only:
            continue
        expected = list(db.connect().execute(c["sql"]).fetchone()) if c["sql"] else []
        t0 = time.time()
        try:
            ans = await agent.ask(c["q"], session=f"eval{i}")
            text = ans.text
        except Exception as e:
            text = f"ERROR {e}"
        res = check(text, expected, c.get("text", False)) if c["sql"] else None
        if res is not None:
            total += 1
            ok += res
        mark = {True: "✅", False: "❌", None: "👁"}[res]
        print(f"\n{mark} [{i}] {c['q']}  ({time.time() - t0:.1f}s)")
        if expected:
            print(f"   kutilgan: {expected}")
        print("   " + text.replace("\n", "\n   "))
        sys.stdout.flush()
        if args.pause:
            await asyncio.sleep(args.pause)
    print(f"\nNatija: {ok}/{total} to'g'ri")


if __name__ == "__main__":
    asyncio.run(main())
