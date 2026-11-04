"""Tovar nomlari, atributlar va kompaniya nomlarini normallashtirish.

Kartochkani sotuvchi to'ldiradi, shuning uchun bitta tovar turlicha yozilgan:
«Хлопок-сырец (спот)» / «ХЛОПОК СЫРЕЦ (СПОТ)», «1-сорта» / «I сорт» / «первый сорт».
Bu yerda ularni yagona ko'rinishga keltiramiz.
"""
import re

# (regex, kanonik nom ruscha, o'zbekcha nom). Tartib muhim: aniqrog'i oldin.
PRODUCTS = [
    (r"масло хлопк|хлопковое масло", "Масло хлопковое", "Paxta yog‘i"),
    (r"шрот", "Шрот хлопковый", "Paxta shroti (kunjara)"),
    (r"пряжа", "Пряжа хлопчатобумажная", "Paxta ipi (kalava)"),
    (r"хлопок", "Хлопок-сырец", "Paxta xomashyosi"),
    (r"проволока", "Проволока арматурная", "Armatura simi"),
    (r"арматур", "Арматура стальная", "Armatura"),
    (r"труб", "Трубы полиэтиленовые (ПЭ)", "Polietilen quvur"),
    (r"полиэтилен", "Полиэтилен", "Polietilen"),
    (r"полипропилен", "Полипропилен", "Polipropilen"),
    (r"поливинилхлорид", "Поливинилхлорид (ПВХ)", "Polivinilxlorid (PVX)"),
    (r"азот", "Азот", "Azot"),
    (r"алюмин", "Профиль алюминиевый", "Alyuminiy profil"),
    (r"селитр", "Аммиачная селитра", "Ammiakli selitra"),
    (r"аргон", "Аргон газообразный", "Argon"),
    (r"бензин", "Бензин автомобильный", "Benzin"),
    (r"битум", "Битум нефтяной", "Bitum"),
    (r"вода", "Вода питьевая", "Ichimlik suvi"),
    (r"газ", "Сжиженный газ (пропан-бутан)", "Suyultirilgan gaz (propan-butan)"),
    (r"гипс", "Гипс строительный", "Gips"),
    (r"дизельн", "Дизельное топливо", "Dizel yoqilg‘isi"),
    (r"известь", "Известь", "Ohak"),
    (r"кабель", "Кабель силовой", "Kuch kabeli"),
    (r"карбамид|мочевин", "Карбамид", "Karbamid (mochevina)"),
    (r"катод", "Катод медный", "Mis katod"),
    (r"кирпич", "Кирпич керамический", "G‘isht (keramik)"),
    (r"кислот", "Кислота серная", "Sulfat kislota"),
    (r"комбикорм|кормосмес", "Комбикорм (кормосмесь)", "Omuxta yem"),
    (r"лист стальн", "Лист стальной горячекатаный", "Po‘lat list (issiq prokat)"),
    (r"мазут", "Мазут топочный", "Mazut"),
    (r"подсолнечн", "Масло подсолнечное", "Kungaboqar yog‘i"),
    (r"мука", "Мука пшеничная", "Bug‘doy uni"),
    (r"пиломатериал", "Пиломатериал обрезной", "Yog‘och-taxta (arralangan)"),
    (r"подшипник", "Подшипник", "Podshipnik"),
    (r"цемент", "Портландцемент", "Sement (portlandsement)"),
    (r"пшениц", "Пшеница продовольственная", "Bug‘doy (oziq-ovqat)"),
    (r"^рис\b", "Рис шлифованный", "Guruch"),
    (r"сахар", "Сахар белый", "Shakar"),
    (r"сода", "Сода каустическая", "Kaustik soda"),
    (r"соль", "Соль пищевая", "Osh tuzi"),
    (r"стекло", "Стекло листовое (флоат)", "Oyna (list shisha)"),
    (r"эмаль", "Эмаль ПФ-115", "Emal (bo‘yoq)"),
]


def canon_product(name: str) -> tuple[str, str]:
    n = re.sub(r"[-\s]+", " ", name.lower()).strip()
    for pat, ru, uz in PRODUCTS:
        if re.search(pat, n):
            return ru, uz
    return name.strip(), name.strip()


_ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4"}
_WORD = {"перв": "1", "втор": "2", "трет": "3"}

SORT_RE = re.compile(
    r"(высш\w*\s+сорт\w*|в/с|(?:перв|втор|трет)\w*\s+сорт\w*|\b(?:iii|ii|i|[123])\s*-?\s*сорт\w*)",
    re.I,
)
CLASS_RE = re.compile(r"\b(iv|iii|ii|i|[1-4])\s*-?\s*класс\w*", re.I)


def norm_sort(v: str | None) -> str | None:
    if not v:
        return None
    s = v.lower().strip()
    if s.startswith("высш") or s == "в/с":
        return "высший"
    for k, d in _WORD.items():
        if s.startswith(k):
            return d
    m = re.match(r"(iii|ii|i|[123])", s)
    if m:
        return _ROMAN.get(m.group(1), m.group(1))
    return s


def norm_class(v: str | None) -> str | None:
    if not v:
        return None
    s = v.lower().strip()
    m = re.match(r"(iv|iii|ii|i|[1-4])\b", s)
    if m:
        return _ROMAN.get(m.group(1), m.group(1))
    return v.strip().upper()  # А500С (armatura sinfi)


MARK_RE = re.compile(
    r"(АИ-\d+|ЦЕМ\s+[IV/А-ЯA-Z-]+\s+\d+,\d\s*Н|PP-\d+|HD-\d+|LL-\d+|LD-\d+|PE-\d+|SG-\d+|"
    r"Г-\d|БНД\s+\d+/\d+|ВР-1|NE\s+\d+/\d+|ПФ-115|КС-\d+|ДТ-[А-Я]-К5|ПБ[АТ]|М00К|М0К|М-\d+)",
    re.I,
)
SIZE_RE = re.compile(r"(Ø\s*\d+\s*мм|\d+[хx]\d+(?:[хx]\d+)?\s*мм|\d+\s*мм|\d+,\d\s*л)", re.I)
TYPES = [
    "рафинированное дезодорированное", "рафинированное", "обогащенная витаминно-минеральной смесью",
    "хлебопекарная", "обрезные хвойных пород", "тостированный", "дорожный", "твердая",
    "йодированная", "техническая", "суспензионный",
]


def norm_mark(v: str | None) -> str | None:
    if not v:
        return None
    s = re.sub(r"\s+", " ", v.strip().upper())
    s = re.sub(r"(\d,\d)\s*Н$", r"\1 Н", s)  # ЦЕМ I 42,5Н -> ЦЕМ I 42,5 Н
    return s


def norm_size(v: str | None) -> str | None:
    if not v:
        return None
    s = v.lower().replace(" ", "").replace("x", "х").replace("ø", "Ø")
    return s


def contract_attrs(row: dict) -> dict:
    """Kartochkadan normallashgan atributlar. Ustunlar bo'sh bo'lsa — nomdan ajratamiz."""
    def get(k):  # pandas NaN / bo'sh satr -> None
        v = row.get(k)
        return v.strip() if isinstance(v, str) and v.strip() else None

    name = get("Наименование продукта") or ""
    mark, size, sort, typ, klass = (get("Марка товара"), get("Размер товара"), get("Сорт товара"),
                                    get("Тип товара"), get("Класс товара"))
    if not sort and (m := SORT_RE.search(name)):
        sort = m.group(1)
    if not klass and (m := CLASS_RE.search(name)):
        klass = m.group(0)
    if not mark and (m := MARK_RE.search(name)):
        mark = m.group(1)
    if not size and (m := SIZE_RE.search(name)):
        size = m.group(1)
    if not typ:
        low = name.lower()
        typ = next((t for t in TYPES if t in low), None)
    return {
        "mark": norm_mark(mark),
        "size": norm_size(size),
        "sort": norm_sort(sort),
        "type": typ.lower() if typ else None,
        "class": norm_class(klass),
    }


REGION_RU2UZ = {
    "г. Ташкент": "Toshkent shahri",
    "Ташкентская область": "Toshkent viloyati",
    "Андижанская область": "Andijon viloyati",
    "Бухарская область": "Buxoro viloyati",
    "Джизакская область": "Jizzax viloyati",
    "Кашкадарьинская область": "Qashqadaryo viloyati",
    "Навоийская область": "Navoiy viloyati",
    "Наманганская область": "Namangan viloyati",
    "Самаркандская область": "Samarqand viloyati",
    "Сурхандарьинская область": "Surxondaryo viloyati",
    "Сырдарьинская область": "Sirdaryo viloyati",
    "Ферганская область": "Farg‘ona viloyati",
    "Хорезмская область": "Xorazm viloyati",
    "Республика Каракалпакстан": "Qoraqalpog‘iston Respublikasi",
}

# Qisqa kalit: SQL'da apostrofsiz filtrlash uchun
REGION_KEY = {
    "Toshkent shahri": "toshkent_sh",
    "Toshkent viloyati": "toshkent_v",
    "Andijon viloyati": "andijon",
    "Buxoro viloyati": "buxoro",
    "Jizzax viloyati": "jizzax",
    "Qashqadaryo viloyati": "qashqadaryo",
    "Navoiy viloyati": "navoiy",
    "Namangan viloyati": "namangan",
    "Samarqand viloyati": "samarqand",
    "Surxondaryo viloyati": "surxondaryo",
    "Sirdaryo viloyati": "sirdaryo",
    "Farg‘ona viloyati": "fargona",
    "Xorazm viloyati": "xorazm",
    "Qoraqalpog‘iston Respublikasi": "qoraqalpogiston",
}

_CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j", "з": "z",
    "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh",
    "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "o", "қ": "q", "ғ": "g",
    "ҳ": "h",
}
_LEGAL = r"\b(mas\s?uliyati cheklangan jamiyati|mchj|ooo|aj|xk|qk|ok|oaj|uk|ao|ojsc|llc)\b"


def search_key(text: str | None) -> str:
    """Qidiruv kaliti: kichik harf, kirill -> lotin, apostrof va yuridik shakl olib tashlangan.

    «"КАМЎЛИ ПЛУС" МЧЖ» -> «kamoli plus», «VOXO‘SER TRADE MCHJ» -> «voxoser trade».
    """
    if not text:
        return ""
    s = "".join(_CYR.get(ch, ch) for ch in text.lower())
    s = re.sub(r"[‘’ʻʼ`'\"«»]", "", s)
    s = re.sub(r"[^0-9a-z]+", " ", s)
    s = re.sub(_LEGAL, " ", s)
    return re.sub(r"\s+", " ", s).strip()
