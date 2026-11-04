"""Interfeysdagi tayyor savollarni (tugmalar, kartalar, yillar) oldindan javoblab, urug' keshiga yozadi.

    python -m eval.warm_cache            # hammasi (~40 savol, ~120 Gemini so'rovi)
    python -m eval.warm_cache --limit 10 # birinchi 10 tasi

Natija: dataset/answer_cache_seed.json — repoga commit qiling, Vercel'da ham darhol ishlaydi.
Javoblar avtomatik tekshirilmaydi: yozishdan oldin ko'rib chiqing (skript har birini chop etadi).
"""
import argparse
import asyncio
import json

from dotenv import load_dotenv

load_dotenv()

from app.agent import SEED_FILE, Agent, AllModelsBusy, _norm_q  # noqa: E402

UZ = [
    "2025-yilda nechta bitim tuzilgan?", "Yillar bo‘yicha bitimlar sonini taqqosla.",
    "Datasetda qanday ma’lumotlar mavjud?", "2025-yilda eng ko‘p savdo qilingan 5 ta tovar qaysi?",
    "2025-yilda oylar bo‘yicha bitimlar soni va savdo aylanmasi qanday bo‘lgan?",
    "2024-yilda karbamidning 1 tonnasi oylar bo‘yicha o‘rtacha qanchadan sotilgan?",
    "2025-yilda savdo summasi bo‘yicha eng yirik 5 ta xaridor kim?",
    "2026-yilda bitimlar holati bo‘yicha qanday taqsimlangan (ijro etilgan, bekor qilingan, qisman va h.k.)?",
    "Yillar bo‘yicha bitimlar soni va savdo aylanmasini taqqosla.",
    "Shartnomalar tovar kategoriyalari bo‘yicha qanday taqsimlangan?",
    "Bitimlar soni bo‘yicha eng faol 5 ta xaridor kim?",
    "Bitimlar soni bo‘yicha top-5 broker (xaridor tomonida) kim?",
    "Yillar bo‘yicha bitimlar soni qanday o‘zgargan va o‘sish sur’ati qancha?",
    "Yillar bo‘yicha savdo aylanmasi so‘mda qanday o‘zgargan?",
    "Yillar bo‘yicha bekor qilingan bitimlar ulushi qanday o‘zgargan?",
] + [f"{y}-yil bo‘yicha asosiy ko‘rsatkichlar: bitimlar soni, aylanma, bekor qilinganlar ulushi va eng ko‘p sotilgan tovar."
     for y in range(2022, 2027)]
RU = [
    "Сколько сделок заключено в 2025 году?", "Сравни количество сделок по годам.",
    "Какие данные доступны в датасете?", "Топ-5 товаров по объёму торгов в 2025 году",
    "Каким было количество сделок и оборот по месяцам в 2025 году?",
    "Какова средняя цена тонны карбамида по месяцам в 2024 году?",
    "Кто 5 крупнейших покупателей по сумме сделок в 2025 году?",
    "Как распределились сделки 2026 года по статусам (исполнены, аннулированы, частично и т.д.)?",
    "Сравни количество сделок и оборот по годам.", "Как контракты распределены по категориям товаров?",
    "Кто 5 самых активных покупателей по числу сделок?", "Топ-5 брокеров покупателя по числу сделок.",
    "Как менялось количество сделок по годам и каковы темпы роста?",
    "Как менялся оборот торгов в сумах по годам?", "Как менялась доля аннулированных сделок по годам?",
] + [f"Основные показатели за {y} год: число сделок, оборот, доля аннулированных и самый продаваемый товар."
     for y in range(2022, 2027)]


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    seed = json.loads(SEED_FILE.read_text()) if SEED_FILE.exists() else {}
    todo = [q for q in UZ + RU if _norm_q(q) not in seed][: args.limit]
    print(f"Urug'da {len(seed)} ta javob bor, {len(todo)} ta yangi savol")
    agent = Agent()
    for i, q in enumerate(todo, 1):
        try:
            ans = await agent.ask(q, session=f"warm{i}")
        except AllModelsBusy:
            print("Limit tugadi — qolganini keyinroq ishga tushiring")
            break
        cached = agent.cache.get(agent._cache_key(q))
        if cached:  # "Kechirasiz…" kabi muvaffaqiyatsiz javoblar keshlanmaydi
            seed[_norm_q(q)] = cached
            SEED_FILE.write_text(json.dumps(seed, ensure_ascii=False, indent=0))
        print(f"\n[{i}/{len(todo)}] {q}  ({ans.model}, {ans.seconds}s)\n  " + ans.text.replace("\n", "\n  "))
    print(f"\nTayyor: {SEED_FILE} ({len(seed)} ta javob)")


if __name__ == "__main__":
    asyncio.run(main())
