"""Interfeys tugmalaridagi tayyor savollar uchun javoblarni AI'siz, to'g'ridan-to'g'ri SQL bilan tuzadi.

    python -m eval.build_presets

Natija dataset/answer_cache_seed.json ga qo'shiladi (AI tekshirgan javoblar saqlanib qoladi). Tugmalar
Gemini limitidan qat'i nazar bir zumda va aniq javob beradi; erkin savollar avvalgidek AI orqali ishlaydi.
"""
import json

from app import db
from app.agent import SEED_FILE, _norm_q

MONTHS = {
    "uz": ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"],
    "ru": ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
}
MONTHS_RU_PREP = ["январе", "феврале", "марте", "апреле", "мае", "июне", "июле", "августе", "сентябре", "октябре", "ноябре", "декабре"]
STATUS_UZ = {
    "Исполнен": "ijro etilgan", "Исполнен(Частично)": "qisman ijro etilgan", "Аннулирован(Не оплачен)": "bekor qilingan (to‘lanmagan)",
    "Оплачен": "to‘langan, yetkazilmagan", "Заключен": "tuzilgan (forvard/fyuchers)", "Ждёт оплату": "to‘lov kutilmoqda",
    "Новый": "yangi (30.10.2026)", "Не подписан": "imzolanmagan",
}
STATUS_RU = {"Исполнен(Частично)": "Исполнен частично", "Аннулирован(Не оплачен)": "Аннулирован (не оплачен)"}
CAT_UZ = {
    "Сельскохозяйственная продукция": "qishloq xo‘jaligi mahsulotlari", "Продовольственные товары": "oziq-ovqat mahsulotlari",
    "Строительные материалы": "qurilish materiallari", "Нефтепродукты": "neft mahsulotlari", "Химическая продукция": "kimyo mahsulotlari",
    "Металлопродукция": "metall mahsulotlari", "Промышленные товары": "sanoat tovarlari", "Полимерная продукция": "polimer mahsulotlari",
}
NOTE_CANCEL = {"uz": "Aylanma bekor qilingan (to‘lanmagan) bitimlarsiz hisoblangan.",
               "ru": "Оборот рассчитан без аннулированных (неоплаченных) сделок."}
NOTE_2026 = {"uz": "2026-yil ma’lumotlari 30-oktabrgacha.", "ru": "Данные за 2026 год — по 30 октября."}


def n(v):
    return f"{int(round(v)):,}".replace(",", " ")


def money(v, lang):
    for div, uz, ru in ((1e12, "trln", "трлн"), (1e9, "mlrd", "млрд"), (1e6, "mln", "млн")):
        if abs(v) >= div:
            num = f"{v / div:.2f}".replace(".", ",")
            return f"{num} {uz} so‘m" if lang == "uz" else f"{num} {ru} сум"
    return f"{n(v)} so‘m" if lang == "uz" else f"{n(v)} сум"


def pct(v):
    return f"{v:.1f}".replace(".", ",") + "%"


def run(sql, params=None):
    """SQL ni agent bilan bir xil formatda bajaradi (veb jadval va grafik uchun)."""
    for i, p in enumerate(params or []):
        sql = sql.replace(f"${i + 1}", repr(p) if isinstance(p, str) else str(p))
    res = db.query(sql)
    assert "error" not in res, (sql, res)
    return sql, res


def answer(text, *queries):
    sqls = [q for q, _ in queries]
    tables = [dict(r, sql=q) for q, r in queries]
    return {"text": text, "sql": sqls, "table": tables[-1] if tables else None, "tables": tables,
            "steps": 1, "seconds": 0.0, "model": "tayyor SQL"}


# ---------------- shablonlar ----------------
def t_dataset(lang):
    q = run("""select (select count(*) from deals) deals, (select count(*) from contracts) contracts,
                      (select count(*) from companies) companies,
                      (select count(*) from companies where role = 'Продавец') sellers,
                      (select count(*) from brokers) brokers, (select count(distinct product) from contracts) products,
                      (select count(distinct product_raw) from contracts) raw_names,
                      (select count(distinct region) from deals) regions""")
    d = dict(zip(q[1]["columns"], q[1]["rows"][0]))
    if lang == "uz":
        text = (f"Dataset — tovar-xomashyo birjasi bitimlari reyestri (barcha ma’lumotlar sun’iy):\n"
                f"- **{n(d['deals'])} ta bitim** — 2022-yil 3-yanvardan 2026-yil 30-oktabrgacha\n"
                f"- **{n(d['contracts'])} ta shartnoma** kartochkasi: tovar, atributlar, valyuta, to‘lov va yetkazish muddatlari\n"
                f"- **{n(d['companies'])} ta kompaniya** ({n(d['sellers'])} sotuvchi, {n(d['companies'] - d['sellers'])} xaridor) va **{d['brokers']} ta broker**\n"
                f"- **{d['products']} ta tovar** ({d['raw_names']} xil yozuvdan normallashtirilgan), {d['regions']} ta hudud\n"
                f"- Har kun uchun dollar kursi; eksport bitimlari USD da\n"
                f"Har bir bitimda: sana va vaqt, tovar, hajm, summa, boshlang‘ich narx, savdo turi (kim oshdi, teskari yoki ikki tomonlama auksion), "
                f"holat, sotuvchi va xaridor, ularning brokerlari, to‘lov va yetkazib berish sanalari.")
    else:
        text = (f"Датасет — реестр сделок товарно-сырьевой биржи (все данные синтетические):\n"
                f"- **{n(d['deals'])} сделок** — с 3 января 2022 по 30 октября 2026\n"
                f"- **{n(d['contracts'])} карточек контрактов**: товар, атрибуты, валюта, сроки оплаты и поставки\n"
                f"- **{n(d['companies'])} компаний** ({n(d['sellers'])} продавцов, {n(d['companies'] - d['sellers'])} покупателей) и **{d['brokers']} брокеров**\n"
                f"- **{d['products']} товар** (нормализовано из {d['raw_names']} вариантов написания), {d['regions']} регионов\n"
                f"- Курс доллара на каждый день; экспортные сделки — в USD\n"
                f"В каждой сделке: дата и время, товар, объём, сумма, стартовая цена, тип торгов (английский, обратный или двусторонний аукцион), "
                f"статус, продавец и покупатель, их брокеры, даты оплаты и поставки.")
    return answer(text, q)


def t_count_year(lang, y):
    q = run("""select count(*) deals, count(*) filter (where is_cancelled) cancelled,
                      sum(amount_uzs) filter (where not is_cancelled) turnover_uzs from deals where year = $1""", [y])
    d, c, tv = q[1]["rows"][0]
    if lang == "uz":
        text = (f"{y}-yilda jami **{n(d)} ta** bitim tuzilgan.\n- Bekor qilingan (to‘lanmagan): **{n(c)} ta** ({pct(c / d * 100)})\n"
                f"- Amalga oshgan bitimlar aylanmasi: **{money(tv, lang)}**")
    else:
        text = (f"В {y} году заключено **{n(d)} сделок**.\n- Аннулировано (не оплачено): **{n(c)}** ({pct(c / d * 100)})\n"
                f"- Оборот состоявшихся сделок: **{money(tv, lang)}**")
    return answer(text, q)


def yearly(cols="deals, turnover, cancel"):
    return run("""select year, count(*) deals, count(*) filter (where is_cancelled) cancelled,
                         round(100.0 * count(*) filter (where is_cancelled) / count(*), 2) cancelled_pct,
                         sum(amount_uzs) filter (where not is_cancelled) turnover_uzs
                  from deals group by 1 order by 1""")


def t_yearly_counts(lang):
    q = yearly()
    rows = q[1]["rows"]
    lines = [f"- **{y}**: {n(d)} ta bitim" if lang == "uz" else f"- **{y}**: {n(d)} сделок" for y, d, *_ in rows]
    best = max(rows, key=lambda r: r[1])
    head = "Yillar bo‘yicha bitimlar soni:" if lang == "uz" else "Количество сделок по годам:"
    tail = (f"Eng ko‘p bitim **{best[0]}-yilda** ({n(best[1])} ta). " if lang == "uz"
            else f"Больше всего сделок — **в {best[0]} году** ({n(best[1])}). ") + NOTE_2026[lang]
    return answer("\n".join([head, *lines, tail]), q)


def t_yearly_full(lang):
    q = yearly()
    rows = q[1]["rows"]
    if lang == "uz":
        lines = [f"- **{y}**: {n(d)} ta bitim, aylanma **{money(tv, lang)}**, bekor qilingan {pct(cp)}" for y, d, c, cp, tv in rows]
        head = "Yillar bo‘yicha bitimlar soni va savdo aylanmasi:"
    else:
        lines = [f"- **{y}**: {n(d)} сделок, оборот **{money(tv, lang)}**, аннулировано {pct(cp)}" for y, d, c, cp, tv in rows]
        head = "Количество сделок и оборот по годам:"
    return answer("\n".join([head, *lines, NOTE_CANCEL[lang] + " " + NOTE_2026[lang]]), q)


def t_yearly_growth(lang):
    q = run("""select year, count(*) deals,
                      round(100.0 * (count(*) - lag(count(*)) over (order by year)) / lag(count(*)) over (order by year), 2) growth_pct
               from deals group by 1 order by 1""")
    rows = q[1]["rows"]
    lines = []
    for y, d, g in rows:
        gs = "" if g is None else (f" ({'+' if g >= 0 else ''}{pct(g)})")
        lines.append(f"- **{y}**: {n(d)} ta{gs}" if lang == "uz" else f"- **{y}**: {n(d)}{gs}")
    full = [r for r in rows if r[0] < 2026]
    cagr = ((full[-1][1] / full[0][1]) ** (1 / (len(full) - 1)) - 1) * 100
    if lang == "uz":
        text = "\n".join(["Yillar bo‘yicha bitimlar soni va o‘tgan yilga nisbatan o‘sish:", *lines,
                          f"2022–2025-yillarda o‘rtacha yillik o‘sish **{pct(cagr)}**. 2026-yil to‘liq emas (30-oktabrgacha), shuning uchun uning pasayishi yil tugamaganidan."])
    else:
        text = "\n".join(["Количество сделок по годам и рост к предыдущему году:", *lines,
                          f"Среднегодовой рост за 2022–2025 — **{pct(cagr)}**. 2026 год неполный (по 30 октября), поэтому снижение связано с незавершённым годом."])
    return answer(text, q)


def t_yearly_turnover(lang):
    q = run("""select year, sum(amount_uzs) filter (where not is_cancelled) turnover_uzs,
                      round(100.0 * (sum(amount_uzs) filter (where not is_cancelled)
                            - lag(sum(amount_uzs) filter (where not is_cancelled)) over (order by year))
                            / lag(sum(amount_uzs) filter (where not is_cancelled)) over (order by year), 2) growth_pct
               from deals group by 1 order by 1""")
    lines = []
    for y, tv, g in q[1]["rows"]:
        gs = "" if g is None else f" ({'+' if g >= 0 else ''}{pct(g)})"
        lines.append(f"- **{y}**: {money(tv, lang)}{gs}")
    head = "Yillar bo‘yicha savdo aylanmasi (so‘mda) va o‘tgan yilga nisbatan o‘zgarish:" if lang == "uz" else "Оборот торгов в сумах по годам и изменение к предыдущему году:"
    return answer("\n".join([head, *lines, NOTE_CANCEL[lang] + " " + NOTE_2026[lang]]), q)


def t_yearly_cancel(lang):
    q = yearly()
    rows = q[1]["rows"]
    lines = [(f"- **{y}**: {n(c)} ta bekor qilingan / {n(d)} ta — **{pct(cp)}**" if lang == "uz"
              else f"- **{y}**: аннулировано {n(c)} из {n(d)} — **{pct(cp)}**") for y, d, c, cp, tv in rows]
    head = "Yillar bo‘yicha bekor qilingan (muddatida to‘lanmagan) bitimlar ulushi:" if lang == "uz" else "Доля аннулированных (не оплаченных в срок) сделок по годам:"
    lo, hi = min(r[3] for r in rows), max(r[3] for r in rows)
    tail = (f"Ulush barqaror: {pct(lo)} dan {pct(hi)} gacha." if lang == "uz" else f"Доля стабильна: от {pct(lo)} до {pct(hi)}.")
    return answer("\n".join([head, *lines, tail]), q)


def t_monthly(lang, y):
    q = run("""select month, count(*) deals, sum(amount_uzs) filter (where not is_cancelled) turnover_uzs
               from deals where year = $1 group by 1 order by 1""", [y])
    rows = q[1]["rows"]
    lines = [(f"- {MONTHS[lang][m - 1].capitalize()}: {n(d)} ta bitim, {money(tv, lang)}" if lang == "uz"
              else f"- {MONTHS[lang][m - 1].capitalize()}: {n(d)} сделок, {money(tv, lang)}") for m, d, tv in rows]
    best = max(rows, key=lambda r: r[2])
    if lang == "uz":
        text = "\n".join([f"{y}-yilda oylar bo‘yicha bitimlar soni va aylanma:", *lines,
                          f"Eng yuqori aylanma — **{MONTHS[lang][best[0] - 1]}** ({money(best[2], lang)}). {NOTE_CANCEL[lang]}"])
    else:
        text = "\n".join([f"Количество сделок и оборот по месяцам в {y} году:", *lines,
                          f"Максимальный оборот — **{MONTHS[lang][best[0] - 1]}** ({money(best[2], lang)}). {NOTE_CANCEL[lang]}"])
    return answer(text, q)


def t_price_monthly(lang, product, y):
    q = run("""select month, round(sum(amount) / sum(volume), 2) avg_price_uzs, sum(volume) volume_tonnes, count(*) deals
               from deals where product = $1 and year = $2 and not is_cancelled and unit = 'тонна' and currency = 'UZS'
               group by 1 order by 1""", [product, y])
    rows = q[1]["rows"]
    lines = [f"- {MONTHS[lang][m - 1].capitalize()}: **{n(p)}** {'so‘m/t' if lang == 'uz' else 'сум/т'} ({n(v)} {'t' if lang == 'uz' else 'т'})" for m, p, v, d in rows]
    lo, hi = min(rows, key=lambda r: r[1]), max(rows, key=lambda r: r[1])
    avg = sum(r[1] * r[2] for r in rows) / sum(r[2] for r in rows)
    if lang == "uz":
        text = "\n".join([f"{y}-yilda karbamidning 1 tonnasi oylar bo‘yicha o‘rtacha narxi (vaznli):", *lines,
                          f"Yillik o‘rtacha — **{n(avg)} so‘m/t**; eng arzon {MONTHS[lang][lo[0] - 1]}da, eng qimmat {MONTHS[lang][hi[0] - 1]}da. Bekor qilingan bitimlar hisobga olinmadi."])
    else:
        text = "\n".join([f"Средняя (взвешенная) цена тонны карбамида по месяцам в {y} году:", *lines,
                          f"Среднегодовая — **{n(avg)} сум/т**; минимум в {MONTHS_RU_PREP[lo[0] - 1]}, максимум в {MONTHS_RU_PREP[hi[0] - 1]}. Аннулированные сделки не учтены."])
    return answer(text, q)


def t_top_buyers(lang, y=None, by="amount"):
    where = f"and d.year = {int(y)}" if y else ""
    order = "turnover_uzs desc" if by == "amount" else "deals desc"
    q = run(f"""select c.name, c.inn, count(*) deals, sum(d.amount_uzs) filter (where not d.is_cancelled) turnover_uzs
                from deals d join companies c on c.inn = d.buyer_inn where true {where}
                group by 1, 2 order by {order} limit 5""")
    rows = q[1]["rows"]
    lines = [(f"{i}. **{nm}** (STIR {inn}) — {money(tv, lang)}, {n(d)} ta bitim" if lang == "uz"
              else f"{i}. **{nm}** (ИНН {inn}) — {money(tv, lang)}, {n(d)} сделок") for i, (nm, inn, d, tv) in enumerate(rows, 1)]
    if lang == "uz":
        head = (f"{y}-yilda savdo summasi bo‘yicha eng yirik 5 ta xaridor:" if by == "amount"
                else "Bitimlar soni bo‘yicha eng faol 5 ta xaridor (2022–2026):")
    else:
        head = (f"5 крупнейших покупателей по сумме сделок в {y} году:" if by == "amount"
                else "5 самых активных покупателей по числу сделок (2022–2026):")
    return answer("\n".join([head, *lines, NOTE_CANCEL[lang]]), q)


def t_top_brokers(lang):
    q = run("""select b.name, b.broker_code, count(*) deals, sum(d.amount_uzs) filter (where not d.is_cancelled) turnover_uzs
               from deals d join brokers b on b.broker_code = d.buyer_broker group by 1, 2 order by deals desc limit 5""")
    rows = q[1]["rows"]
    lines = [(f"{i}. **{nm}** ({code}) — {n(d)} ta bitim, {money(tv, lang)}" if lang == "uz"
              else f"{i}. **{nm}** ({code}) — {n(d)} сделок, {money(tv, lang)}") for i, (nm, code, d, tv) in enumerate(rows, 1)]
    head = "Xaridor tomonidagi bitimlar soni bo‘yicha top-5 broker (2022–2026):" if lang == "uz" else "Топ-5 брокеров покупателя по числу сделок (2022–2026):"
    return answer("\n".join([head, *lines]), q)


def t_status(lang, y):
    q = run("""select status, count(*) deals, round(100.0 * count(*) / sum(count(*)) over (), 2) share_pct
               from deals where year = $1 group by 1 order by 2 desc""", [y])
    rows = q[1]["rows"]
    total = sum(r[1] for r in rows)
    name = (lambda s: STATUS_UZ.get(s, s)) if lang == "uz" else (lambda s: STATUS_RU.get(s, s))
    lines = [f"- {name(s).capitalize()}: **{n(d)}** ({pct(p)})" for s, d, p in rows]
    head = (f"{y}-yilda {n(total)} ta bitim holatlar bo‘yicha (30.10.2026 holatiga):" if lang == "uz"
            else f"{n(total)} сделок {y} года по статусам (на 30.10.2026):")
    return answer("\n".join([head, *lines]), q)


def t_categories(lang):
    q = run("""select category, count(*) contracts, count(distinct product) products
               from contracts group by 1 order by 2 desc""")
    rows = q[1]["rows"]
    total = sum(r[1] for r in rows)
    lines = [(f"- {CAT_UZ.get(c, c).capitalize()}: **{n(k)}** ta ({pct(k / total * 100)}), {p} xil tovar" if lang == "uz"
              else f"- {c}: **{n(k)}** ({pct(k / total * 100)}), товаров: {p}") for c, k, p in rows]
    head = f"{n(total)} ta shartnoma tovar kategoriyalari bo‘yicha:" if lang == "uz" else f"{n(total)} контрактов по категориям товаров:"
    return answer("\n".join([head, *lines]), q)


def t_top_products(lang, y):
    q = run("""select product, product_uz, sum(amount_uzs) filter (where not is_cancelled) turnover_uzs,
                      sum(volume_tonnes) filter (where not is_cancelled) volume_tonnes, count(*) deals
               from deals where year = $1 group by 1, 2 order by turnover_uzs desc limit 5""", [y])
    rows = q[1]["rows"]
    lines = [(f"{i}. **{uz}** — {money(tv, lang)} ({n(vt)} t, {n(d)} ta bitim)" if lang == "uz"
              else f"{i}. **{ru}** — {money(tv, lang)} ({n(vt)} т, {n(d)} сделок)") for i, (ru, uz, tv, vt, d) in enumerate(rows, 1)]
    head = f"{y}-yilda savdo aylanmasi bo‘yicha top-5 tovar:" if lang == "uz" else f"Топ-5 товаров по обороту торгов в {y} году:"
    return answer("\n".join([head, *lines, NOTE_CANCEL[lang]]), q)


def t_year_summary(lang, y):
    q1 = run("""select count(*) deals, count(*) filter (where is_cancelled) cancelled,
                       sum(amount_uzs) filter (where not is_cancelled) turnover_uzs,
                       count(distinct buyer_inn) buyers, count(distinct seller_inn) sellers
                from deals where year = $1""", [y])
    q2 = run("""select product, product_uz, sum(amount_uzs) filter (where not is_cancelled) turnover_uzs, count(*) deals
                from deals where year = $1 group by 1, 2 order by turnover_uzs desc limit 5""", [y])
    d, c, tv, b, s = q1[1]["rows"][0]
    top = q2[1]["rows"][0]
    part = NOTE_2026[lang] if y == 2026 else ""
    if lang == "uz":
        text = (f"{y}-yil bo‘yicha asosiy ko‘rsatkichlar:\n- Bitimlar: **{n(d)} ta**\n- Bekor qilingan: **{n(c)} ta** ({pct(c / d * 100)})\n"
                f"- Savdo aylanmasi: **{money(tv, lang)}**\n- Faol xaridorlar: {n(b)}, sotuvchilar: {n(s)}\n"
                f"- Eng ko‘p sotilgan tovar (aylanma bo‘yicha): **{top[1]}** — {money(top[2], lang)} ({n(top[3])} ta bitim)\n"
                f"{NOTE_CANCEL[lang]} {part}").strip()
    else:
        text = (f"Основные показатели за {y} год:\n- Сделок: **{n(d)}**\n- Аннулировано: **{n(c)}** ({pct(c / d * 100)})\n"
                f"- Оборот торгов: **{money(tv, lang)}**\n- Активных покупателей: {n(b)}, продавцов: {n(s)}\n"
                f"- Самый продаваемый товар (по обороту): **{top[0]}** — {money(top[2], lang)} ({n(top[3])} сделок)\n"
                f"{NOTE_CANCEL[lang]} {part}").strip()
    return answer(text, q1, q2)


def presets():
    P = {}
    for lang, qs in {
        "uz": {
            "Datasetda qanday ma’lumotlar mavjud?": lambda: t_dataset("uz"),
            "2025-yilda oylar bo‘yicha bitimlar soni va savdo aylanmasi qanday bo‘lgan?": lambda: t_monthly("uz", 2025),
            "2024-yilda karbamidning 1 tonnasi oylar bo‘yicha o‘rtacha qanchadan sotilgan?": lambda: t_price_monthly("uz", "Карбамид", 2024),
            "2025-yilda savdo summasi bo‘yicha eng yirik 5 ta xaridor kim?": lambda: t_top_buyers("uz", 2025, "amount"),
            "2026-yilda bitimlar holati bo‘yicha qanday taqsimlangan (ijro etilgan, bekor qilingan, qisman va h.k.)?": lambda: t_status("uz", 2026),
            "Yillar bo‘yicha bitimlar soni va savdo aylanmasini taqqosla.": lambda: t_yearly_full("uz"),
            "Shartnomalar tovar kategoriyalari bo‘yicha qanday taqsimlangan?": lambda: t_categories("uz"),
            "Bitimlar soni bo‘yicha eng faol 5 ta xaridor kim?": lambda: t_top_buyers("uz", None, "count"),
            "Bitimlar soni bo‘yicha top-5 broker (xaridor tomonida) kim?": lambda: t_top_brokers("uz"),
            "Yillar bo‘yicha bitimlar soni qanday o‘zgargan va o‘sish sur’ati qancha?": lambda: t_yearly_growth("uz"),
            "Yillar bo‘yicha savdo aylanmasi so‘mda qanday o‘zgargan?": lambda: t_yearly_turnover("uz"),
            "Yillar bo‘yicha bekor qilingan bitimlar ulushi qanday o‘zgargan?": lambda: t_yearly_cancel("uz"),
            **{f"{y}-yil bo‘yicha asosiy ko‘rsatkichlar: bitimlar soni, aylanma, bekor qilinganlar ulushi va eng ko‘p sotilgan tovar.":
               (lambda y=y: t_year_summary("uz", y)) for y in range(2022, 2027)},
        },
        "ru": {
            "Сколько сделок заключено в 2025 году?": lambda: t_count_year("ru", 2025),
            "Сравни количество сделок по годам.": lambda: t_yearly_counts("ru"),
            "Какие данные доступны в датасете?": lambda: t_dataset("ru"),
            "Топ-5 товаров по объёму торгов в 2025 году": lambda: t_top_products("ru", 2025),
            "Каким было количество сделок и оборот по месяцам в 2025 году?": lambda: t_monthly("ru", 2025),
            "Какова средняя цена тонны карбамида по месяцам в 2024 году?": lambda: t_price_monthly("ru", "Карбамид", 2024),
            "Кто 5 крупнейших покупателей по сумме сделок в 2025 году?": lambda: t_top_buyers("ru", 2025, "amount"),
            "Как распределились сделки 2026 года по статусам (исполнены, аннулированы, частично и т.д.)?": lambda: t_status("ru", 2026),
            "Сравни количество сделок и оборот по годам.": lambda: t_yearly_full("ru"),
            "Как контракты распределены по категориям товаров?": lambda: t_categories("ru"),
            "Кто 5 самых активных покупателей по числу сделок?": lambda: t_top_buyers("ru", None, "count"),
            "Топ-5 брокеров покупателя по числу сделок.": lambda: t_top_brokers("ru"),
            "Как менялось количество сделок по годам и каковы темпы роста?": lambda: t_yearly_growth("ru"),
            "Как менялся оборот торгов в сумах по годам?": lambda: t_yearly_turnover("ru"),
            "Как менялась доля аннулированных сделок по годам?": lambda: t_yearly_cancel("ru"),
            **{f"Основные показатели за {y} год: число сделок, оборот, доля аннулированных и самый продаваемый товар.":
               (lambda y=y: t_year_summary("ru", y)) for y in range(2022, 2027)},
        },
    }.items():
        for q, fn in qs.items():
            P[_norm_q(q)] = fn()
    return P


if __name__ == "__main__":
    seed = json.loads(SEED_FILE.read_text()) if SEED_FILE.exists() else {}
    new = presets()
    added = [q for q in new if q not in seed]
    seed.update({q: v for q, v in new.items() if q not in seed or seed[q].get("model") == "tayyor SQL"})
    SEED_FILE.write_text(json.dumps(seed, ensure_ascii=False, indent=0))
    print(f"Tayyor javoblar: {len(new)} ({len(added)} yangi), urug'da jami {len(seed)}")
    for q in list(new)[:3]:
        print("\n" + q + "\n" + new[q]["text"])
