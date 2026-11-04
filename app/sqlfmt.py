"""SQL ni ko'rsatish uchun: chiroyli formatlash va asosiy so'rov filtrlarini odam tiliga o'girish."""
import re

from app.normalize import REGION_KEY

_REGION_NAMES = {v: k for k, v in REGION_KEY.items()}

_TOK = re.compile(r"'(?:[^']|'')*'|\"[^\"]*\"|\(|\)|,|\s+|[^\s(),'\"]+")
_CLAUSE = {"select", "from", "where", "having", "limit", "with", "union", "qualify", "window"}
_PAIR = {"group", "order"}            # "group by", "order by"
_JOIN_PREFIX = {"left", "inner", "full", "cross", "right"}
_STOP = {"group", "order", "limit", "having", "union", "qualify", "window"}
_SPACE_BEFORE_PAREN = {"in", "as", "and", "or", "not", "from", "join", "exists", "on", "select", "where", "by",
                       "over", "filter", "then", "else", "when", "with", "values", "union", "all"}


def _tokens(sql: str) -> list[str]:
    return _TOK.findall(sql.strip().rstrip(";").strip())


def pretty_sql(sql: str) -> str:
    """Yuqori darajadagi bo'limlarni (SELECT, FROM, WHERE…) yangi qatordan boshlaydi, ichki so'rovlarga tegmaydi."""
    toks = [t for t in _tokens(sql) if not t.isspace()]
    out, depth, in_select, prev = [], 0, False, ""
    for i, t in enumerate(toks):
        low = t.lower()
        nxt = toks[i + 1].lower() if i + 1 < len(toks) else ""
        newline = depth == 0 and out and (
            low in _CLAUSE or (low in _PAIR and nxt == "by") or low in _JOIN_PREFIX
            or (low == "join" and prev not in _JOIN_PREFIX))
        if depth == 0 and low in _CLAUSE | _PAIR | _JOIN_PREFIX | {"join"}:
            in_select = low == "select"
        call = t == "(" and re.fullmatch(r"\w+", prev or "") and prev not in _SPACE_BEFORE_PAREN
        if newline:
            out.append("\n")
        elif out and out[-1] not in ("\n", "(", "\n    ") and t not in (")", ",") and not call:
            out.append(" ")
        out.append(t)
        if t == "(":
            depth += 1
        elif t == ")":
            depth -= 1
        elif t == "," and depth == 0 and in_select:
            out.append("\n    ")
        prev = low
    return "".join(out).replace("( ", "(")


def top_level_where(sql: str) -> list[str]:
    """Asosiy so'rovning WHERE shartlari (AND bo'yicha bo'lingan). Ichki so'rovlardagi shartlar olinmaydi."""
    toks = _tokens(sql)
    depth, conds, cur, inside = 0, [], [], False
    for t in toks:
        low = t.lower()
        if depth == 0 and low == "where":
            inside, cur = True, []
            continue
        if inside and depth == 0 and (low in _STOP or low == "select" or t == ")"):
            inside = False
            conds.append("".join(cur).strip())
            cur = []
        if t == "(":
            depth += 1
        elif t == ")":
            depth -= 1
        if not inside:
            continue
        if depth == 0 and low == "and":
            conds.append("".join(cur).strip())
            cur = []
        else:
            cur.append(t)
    if inside:
        conds.append("".join(cur).strip())
    return [re.sub(r"\s+", " ", c) for c in conds if c and c.lower() != "true"]


_LABELS = {
    "uz": {"year": "yil", "month": "oy", "product": "tovar", "region": "viloyat", "status": "holat", "seller": "sotuvchi STIR",
           "buyer": "xaridor STIR", "deal": "bitim №", "unit": "birlik", "mark": "marka", "sort": "nav", "category": "kategoriya",
           "no_cancel": "bekor qilinganlarsiz", "only_cancel": "faqat bekor qilinganlar", "export": "eksport bitimlari",
           "domestic": "ichki bitimlar", "form": "shartnoma shakli", "trade": "savdo turi", "currency": "valyuta"},
    "ru": {"year": "год", "month": "месяц", "product": "товар", "region": "регион", "status": "статус", "seller": "ИНН продавца",
           "buyer": "ИНН покупателя", "deal": "сделка №", "unit": "единица", "mark": "марка", "sort": "сорт", "category": "категория",
           "no_cancel": "без аннулированных", "only_cancel": "только аннулированные", "export": "экспортные сделки",
           "domestic": "внутренние сделки", "form": "форма контракта", "trade": "тип торгов", "currency": "валюта"},
}
_COLS = {"year": "year", "month": "month", "product": "product", "region_key": "region", "region": "region", "status": "status",
         "seller_inn": "seller", "buyer_inn": "buyer", "deal_id": "deal", "unit": "unit", "mark": "mark", "sort": "sort",
         "category": "category", "contract_form": "form", "trade_type": "trade", "currency": "currency"}


def humanize(cond: str, lang: str = "uz") -> dict:
    """Bitta shartni odam tiliga: {'text': ..., 'code': False} yoki o'zgartirib bo'lmasa {'text': shart, 'code': True}."""
    L = _LABELS["ru" if lang == "ru" else "uz"]
    c = cond.strip()
    while c.startswith("(") and c.endswith(")") and c[1:-1].count("(") == c[1:-1].count(")"):
        c = c[1:-1].strip()
    c = re.sub(r"(?<!['\w])[a-z]\w*\.(?=[a-z_])", "", c, flags=re.I)  # d.year -> year
    low = c.lower().replace(" ", "")
    if low in ("notis_cancelled", "is_cancelled=false", "is_cancelled=0", "notcoalesce(is_cancelled,false)"):
        return {"text": L["no_cancel"], "code": False}
    if low in ("is_cancelled", "is_cancelled=true", "is_cancelled=1"):
        return {"text": L["only_cancel"], "code": False}
    m = re.fullmatch(r"extract\(\s*year\s+from\s+deal_date\s*\)\s*=\s*(\d{4})", c, re.I)
    if m:
        return {"text": f"{L['year']}: {m.group(1)}", "code": False}
    m = re.fullmatch(r"contract_type\s*=\s*'(Экспортный|Внутренний)'", c, re.I)
    if m:
        return {"text": L["export"] if m.group(1) == "Экспортный" else L["domestic"], "code": False}
    m = re.fullmatch(r"(\w+)\s*=\s*('(?:[^']|'')*'|\d+)", c)
    if m and m.group(1).lower() in _COLS:
        val = m.group(2).strip("'")
        key = _COLS[m.group(1).lower()]
        if m.group(1).lower() == "region_key":
            val = _REGION_NAMES.get(val, val)
        return {"text": f"{L[key]}{val}" if key == "deal" else f"{L[key]}: {val}", "code": False}
    m = re.fullmatch(r"(\w+)\s+between\s+(\S+)\s+and\s+(\S+)", c, re.I)
    if m and m.group(1).lower() in _COLS:
        return {"text": f"{L[_COLS[m.group(1).lower()]]}: {m.group(2).strip(chr(39))}–{m.group(3).strip(chr(39))}", "code": False}
    m = re.fullmatch(r"(\w+)\s+in\s*\((.+)\)", c, re.I)
    if m and m.group(1).lower() in _COLS:
        vals = ", ".join(v.strip().strip("'") for v in m.group(2).split(","))
        return {"text": f"{L[_COLS[m.group(1).lower()]]}: {vals}", "code": False}
    return {"text": cond, "code": True}
