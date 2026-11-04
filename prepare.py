"""CSV -> DuckDB: python prepare.py

Natija: data/uzex.duckdb — inglizcha ustun nomlari, raqam/sana turlari, kanonik tovar nomlari,
so'm/dollarga o'girilgan summalar va kompaniyalar uchun qidiruv kaliti.
Vercel kabi serverless muhitda app.db birinchi so'rovda build() ni /tmp ga chaqiradi.
"""
import csv as csvmod
import sys
import tempfile
import time
import zipfile
from pathlib import Path

import duckdb

from app.normalize import (REGION_KEY, REGION_RU2UZ, canon_product, contract_attrs,
                           search_key)

ROOT = Path(__file__).parent
SRC = ROOT / "data" / "uzex_spot_data"
ZIP = ROOT / "dataset" / "uzex_spot_data.zip"
DB = ROOT / "data" / "uzex.duckdb"


def num(col: str) -> str:
    return f"cast(replace(\"{col}\", ' ', '') as double)"


def dt(col: str) -> str:
    return f"try_strptime(\"{col}\", '%d.%m.%Y')::date"


def _rows(con, sql):
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def _write(path: Path, header: list[str], rows: list[list]):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csvmod.writer(f)
        w.writerow(header)
        w.writerows([["" if v is None else v for v in r] for r in rows])


def build(db_path: Path = DB, src: Path = SRC, zip_path: Path = ZIP, verbose: bool = True) -> Path:
    t0 = time.time()
    work = Path(tempfile.mkdtemp(prefix="uzex_"))
    if not src.exists():
        if not zip_path.exists():
            sys.exit(f"Ma'lumotlar topilmadi: {src} (yoki {zip_path})")
        if verbose:
            print(f"{zip_path.name} ochilmoqda...")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(work)
        src = work / "uzex_spot_data"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = db_path.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    con = duckdb.connect(str(tmp))

    def csv(name):
        return f"read_csv('{src / name}', all_varchar=true, header=true)"

    # --- kurs ---
    con.execute(f"""
        create table usd_rates as
        select strptime("Дата", '%d.%m.%Y')::date as rate_date, cast("Курс" as double) as rate
        from {csv('usd_rates.csv')} order by 1""")

    # --- shartnomalar: normallashtirish Python'da, natija vaqtinchalik CSV orqali ---
    norm = []
    for r in _rows(con, f"select * from {csv('contracts.csv')}"):
        ru, uz = canon_product(r["Наименование продукта"])
        a = contract_attrs(r)
        region = REGION_RU2UZ.get(r["Регион"])
        if region is None:
            sys.exit(f"Noma'lum viloyat: {r['Регион']}")
        norm.append([r["Номер контракта"], ru, uz, a["mark"], a["size"], a["sort"], a["type"], a["class"],
                     region, REGION_KEY[region]])
    _write(work / "c_norm.csv", ["cid", "product", "product_uz", "a_mark", "a_size", "a_sort", "a_type",
                                 "a_class", "region_uz", "region_key"], norm)
    con.execute(f"""
        create table contracts as select
            cast(c."Номер контракта" as bigint) as contract_id,
            c."Наименование продукта" as product_raw,
            n.product, n.product_uz,
            n.a_mark as mark, n.a_size as size, n.a_sort as sort, n.a_type as type, n.a_class as class,
            concat_ws(', ', n.product,
                case when n.a_mark is not null then 'марка ' || n.a_mark end,
                case when n.a_size is not null then n.a_size end,
                case when n.a_sort = 'высший' then 'высший сорт' when n.a_sort is not null then n.a_sort || ' сорт' end,
                case when n.a_class is not null and n.a_class similar to '[1-4]' then n.a_class || ' класс'
                     when n.a_class is not null then 'класс ' || n.a_class end,
                n.a_type) as product_spec,
            c."Код ТН ВЭД" as hs_code,
            c."Группа товара" as product_group,
            c."Категория товара" as category,
            c."Отрасль промышленности" as industry,
            c."Единица измерения" as unit,
            cast(c."Лот" as integer) as lot_size,
            case c."Валюта" when 'Доллар США' then 'USD' else 'UZS' end as currency,
            {num('Базисная цена')} as base_price,
            cast(replace(c."Сумма залога", ' %', '') as double) as deposit_pct,
            c."Базис поставки" as delivery_basis,
            c."Упаковка" as packaging,
            n.region_uz as region, n.region_key,
            c."Адрес склада" as warehouse_address,
            c."Тип торгов" as trade_type,
            c."Тип контракта" as contract_type,
            c."Форма контракта" as contract_form,
            cast(c."Срок оплаты" as integer) as payment_term_days,
            cast(c."Срок поставки" as integer) as delivery_term_days,
            c."ИНН продавца" as seller_inn,
            {dt('Дата регистрации')} as reg_date,
            {dt('Действует до')} as valid_until
        from {csv('contracts.csv')} c
        join read_csv('{work / "c_norm.csv"}', all_varchar=true, header=true) n on n.cid = c."Номер контракта"
        order by contract_id""")

    # --- kompaniyalar va brokerlar ---
    parts = _rows(con, f'select "ИНН", "Наименование", "Регион" from {csv("participants.csv")}')
    _write(work / "p_norm.csv", ["inn", "name_key", "region_key"],
           [[r["ИНН"], search_key(r["Наименование"]), REGION_KEY.get(r["Регион"])] for r in parts])
    con.execute(f"""
        create table companies as select
            p."ИНН" as inn, p."Наименование" as name, n.name_key, p."Регион" as region, n.region_key,
            p."Вид деятельности" as activity, p."Роль" as role, p."Плательщик НДС" = 'Да' as vat_payer
        from {csv('participants.csv')} p
        join read_csv('{work / "p_norm.csv"}', all_varchar=true, header=true) n on n.inn = p."ИНН"
        order by inn""")

    brk = _rows(con, f'select "Код брокера", "Наименование", "Регион" from {csv("brokers.csv")}')
    _write(work / "b_norm.csv", ["code", "name_key", "region_key"],
           [[r["Код брокера"], search_key(r["Наименование"]), REGION_KEY.get(r["Регион"])] for r in brk])
    con.execute(f"""
        create table brokers as select
            b."Код брокера" as broker_code, b."Наименование" as name, n.name_key, b."ИНН" as inn,
            b."Регион" as region, n.region_key
        from {csv('brokers.csv')} b
        join read_csv('{work / "b_norm.csv"}', all_varchar=true, header=true) n on n.code = b."Код брокера"
        order by broker_code""")

    # --- bitimlar ---
    con.execute(f"""
        create table deals as
        with d as (select * from {csv('deals_*.csv')})
        select
            cast(d."Номер сделки" as bigint) as deal_id,
            {dt('Дата сделки')} as deal_date,
            cast(d."Время сделки" as time) as deal_time,
            year({dt('Дата сделки')}) as year,
            month({dt('Дата сделки')}) as month,
            d."Тип торгов" as trade_type,
            cast(d."Количество" as bigint) as qty_lots,
            cast(d."Лот" as integer) as lot_size,
            d."Единица измерения" as unit,
            cast(d."Количество" as bigint) * cast(d."Лот" as integer) as volume,
            case d."Единица измерения" when 'тонна' then cast(d."Количество" as bigint) * cast(d."Лот" as integer)
                 when 'килограмм' then cast(d."Количество" as bigint) * cast(d."Лот" as integer) / 1000.0 end as volume_tonnes,
            {num('Сумма сделки')} as amount,
            c.currency,
            r.rate as usd_rate,
            case c.currency when 'USD' then {num('Сумма сделки')} * r.rate else {num('Сумма сделки')} end as amount_uzs,
            case c.currency when 'USD' then {num('Сумма сделки')} else {num('Сумма сделки')} / r.rate end as amount_usd,
            {num('Стартовая цена')} as start_price,
            {num('Сумма сделки')} / (cast(d."Количество" as bigint) * cast(d."Лот" as integer)) as unit_price,
            case c.currency when 'USD' then r.rate else 1 end
                * {num('Сумма сделки')} / (cast(d."Количество" as bigint) * cast(d."Лот" as integer)) as unit_price_uzs,
            cast(d."Номер контракта" as bigint) as contract_id,
            d."Наименование товара" as product_raw,
            c.product, c.product_uz, c.product_spec,
            c.mark, c.size, c.sort, c.type, c.class,
            c.category, c.product_group, c.industry, c.hs_code,
            d."Регион" as region,
            c.region_key,
            d."Тип контракта" as contract_type,
            d."Форма контракта" as contract_form,
            d."Состояние сделки" as status,
            d."Состояние сделки" = 'Аннулирован(Не оплачен)' as is_cancelled,
            d."ИНН продавца" as seller_inn,
            d."ИНН покупателя" as buyer_inn,
            d."Брокер продавца" as seller_broker,
            d."Брокер покупателя" as buyer_broker,
            {dt('Дата оплаты')} as payment_date,
            {dt('Дата поставки')} as delivery_date,
            cast(d."Поставлено" as bigint) as delivered_lots,
            cast(d."Поставлено" as bigint) * cast(d."Лот" as integer) as delivered_volume
        from d
        join contracts c on c.contract_id = cast(d."Номер контракта" as bigint)
        join usd_rates r on r.rate_date = {dt('Дата сделки')}
        order by deal_id""")

    # Tekshiruvlar
    n = con.execute("select count(*) from deals").fetchone()[0]
    bad_region = con.execute("""select count(*) from deals d join contracts c using(contract_id)
                                where d.region <> c.region""").fetchone()[0]
    nulls = con.execute("select count(*) from deals where amount is null or deal_date is null or usd_rate is null").fetchone()[0]
    if verbose:
        print(f"deals={n}, region mos kelmagan={bad_region}, bo'sh qiymat={nulls}")
        print(con.execute("select product, count(*) from contracts group by 1 order by 2 desc").fetchall())

    for t, cols in {"deals": ["deal_date", "product", "seller_inn", "buyer_inn", "contract_id"],
                    "companies": ["inn"], "contracts": ["contract_id"]}.items():
        for c in cols:
            con.execute(f"create index idx_{t}_{c} on {t}({c})")
    con.close()
    tmp.replace(db_path)
    for f in sorted(work.rglob("*"), reverse=True):
        f.unlink() if f.is_file() else f.rmdir()
    work.rmdir()
    if verbose:
        print(f"Tayyor: {db_path} ({db_path.stat().st_size / 1e6:.0f} MB, {time.time() - t0:.1f} s)")
    return db_path


if __name__ == "__main__":
    build()
