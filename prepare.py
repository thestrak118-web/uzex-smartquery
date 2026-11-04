"""CSV -> DuckDB. Bir marta ishga tushiriladi: python prepare.py

Natija: data/uzex.duckdb — inglizcha ustun nomlari, raqam/sana turlari, kanonik tovar nomlari,
so'm/dollarga o'girilgan summalar va kompaniyalar uchun qidiruv kaliti.
"""
import sys
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


def main():
    if not SRC.exists() and ZIP.exists():
        print(f"{ZIP.name} ochilmoqda...")
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(SRC.parent)
    if not SRC.exists():
        sys.exit(f"Ma'lumotlar topilmadi: {SRC} (yoki {ZIP})")
    t0 = time.time()
    tmp = DB.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    con = duckdb.connect(str(tmp))

    def csv(name):
        return f"read_csv('{SRC / name}', all_varchar=true, header=true)"

    # --- kurs ---
    con.execute(f"""
        create table usd_rates as
        select strptime("Дата", '%d.%m.%Y')::date as rate_date, cast("Курс" as double) as rate
        from {csv('usd_rates.csv')} order by 1""")

    # --- shartnomalar ---
    raw = con.execute(f"select * from {csv('contracts.csv')}").fetchdf()
    canon = raw["Наименование продукта"].map(canon_product)
    raw["product"] = canon.map(lambda x: x[0])
    raw["product_uz"] = canon.map(lambda x: x[1])
    attrs = raw.apply(lambda r: contract_attrs(r.to_dict()), axis=1, result_type="expand")
    for c in ["mark", "size", "sort", "type", "class"]:
        raw["a_" + c] = attrs[c]
    raw["region_uz"] = raw["Регион"].map(REGION_RU2UZ)
    if raw["region_uz"].isna().any():
        sys.exit(f"Noma'lum viloyat: {raw.loc[raw['region_uz'].isna(), 'Регион'].unique()}")
    raw["region_key"] = raw["region_uz"].map(REGION_KEY)
    con.register("c_raw", raw)
    con.execute(f"""
        create table contracts as select
            cast("Номер контракта" as bigint) as contract_id,
            "Наименование продукта" as product_raw,
            product, product_uz,
            a_mark as mark, a_size as size, a_sort as sort, a_type as type, a_class as class,
            concat_ws(', ', product,
                case when a_mark is not null then 'марка ' || a_mark end,
                case when a_size is not null then a_size end,
                case when a_sort = 'высший' then 'высший сорт' when a_sort is not null then a_sort || ' сорт' end,
                case when a_class is not null and a_class similar to '[1-4]' then a_class || ' класс'
                     when a_class is not null then 'класс ' || a_class end,
                a_type) as product_spec,
            "Код ТН ВЭД" as hs_code,
            "Группа товара" as product_group,
            "Категория товара" as category,
            "Отрасль промышленности" as industry,
            "Единица измерения" as unit,
            cast("Лот" as integer) as lot_size,
            case "Валюта" when 'Доллар США' then 'USD' else 'UZS' end as currency,
            {num('Базисная цена')} as base_price,
            cast(replace("Сумма залога", ' %', '') as double) as deposit_pct,
            "Базис поставки" as delivery_basis,
            "Упаковка" as packaging,
            region_uz as region, region_key,
            "Адрес склада" as warehouse_address,
            "Тип торгов" as trade_type,
            "Тип контракта" as contract_type,
            "Форма контракта" as contract_form,
            cast("Срок оплаты" as integer) as payment_term_days,
            cast("Срок поставки" as integer) as delivery_term_days,
            "ИНН продавца" as seller_inn,
            {dt('Дата регистрации')} as reg_date,
            {dt('Действует до')} as valid_until
        from c_raw""")
    con.unregister("c_raw")

    # --- kompaniyalar va brokerlar ---
    parts = con.execute(f"select * from {csv('participants.csv')}").fetchdf()
    parts["name_key"] = parts["Наименование"].map(search_key)
    parts["region_key"] = parts["Регион"].map(REGION_KEY)
    con.register("p_raw", parts)
    con.execute("""
        create table companies as select
            "ИНН" as inn, "Наименование" as name, name_key, "Регион" as region, region_key,
            "Вид деятельности" as activity, "Роль" as role, "Плательщик НДС" = 'Да' as vat_payer
        from p_raw""")
    con.unregister("p_raw")

    brk = con.execute(f"select * from {csv('brokers.csv')}").fetchdf()
    brk["name_key"] = brk["Наименование"].map(search_key)
    brk["region_key"] = brk["Регион"].map(REGION_KEY)
    con.register("b_raw", brk)
    con.execute("""
        create table brokers as select
            "Код брокера" as broker_code, "Наименование" as name, name_key, "ИНН" as inn,
            "Регион" as region, region_key
        from b_raw""")
    con.unregister("b_raw")

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
    print(f"deals={n}, region mos kelmagan={bad_region}, bo'sh qiymat={nulls}")
    print(con.execute("select product, count(*) from contracts group by 1 order by 2 desc").fetchall())

    for t, cols in {"deals": ["deal_date", "product", "seller_inn", "buyer_inn", "contract_id"],
                    "companies": ["inn"], "contracts": ["contract_id"]}.items():
        for c in cols:
            con.execute(f"create index idx_{t}_{c} on {t}({c})")
    con.close()
    tmp.replace(DB)
    print(f"Tayyor: {DB} ({DB.stat().st_size / 1e6:.0f} MB, {time.time() - t0:.1f} s)")


if __name__ == "__main__":
    main()
