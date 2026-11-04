"""Test savollar: savol + to'g'ri javobni hisoblaydigan SQL.

`expect` — javob matnida bo'lishi kerak bo'lgan son(lar) yoki satr(lar). Sonlar 1% aniqlikda tekshiriladi.
"""

CASES = [
    {"q": "2025-yilda nechta bitim tuzilgan?",
     "sql": "select count(*) from deals where year = 2025"},
    {"q": "Сколько сделок было аннулировано в 2024 году?",
     "sql": "select count(*) from deals where year = 2024 and is_cancelled"},
    {"q": "2023-yilda umumiy savdo aylanmasi so‘mda qancha bo‘lgan?",
     "sql": "select sum(amount_uzs) from deals where year = 2023 and not is_cancelled"},
    {"q": "Какой товар был лидером по сумме сделок в 2025 году?",
     "sql": """select product from deals where year = 2025 and not is_cancelled
               group by 1 order by sum(amount_uzs) desc limit 1""", "text": True},
    {"q": "2024-yilda karbamidning 1 tonnasi o‘rtacha qanchadan sotilgan?",
     "sql": """select sum(amount) / sum(volume) from deals
               where year = 2024 and product = 'Карбамид' and not is_cancelled"""},
    {"q": "Qaysi viloyatda 2026-yilda eng ko‘p bitim tuzilgan?",
     "sql": "select region from deals where year = 2026 group by 1 order by count(*) desc limit 1", "text": True},
    {"q": "Какой брокер покупателя заключил больше всего сделок?",
     "sql": """select b.name from deals d join brokers b on b.broker_code = d.buyer_broker
               group by 1 order by count(*) desc limit 1""", "text": True},
    {"q": "STIR 921912462 bo‘lgan kompaniya jami qancha summaga mahsulot sotgan?",
     "sql": "select sum(amount_uzs) from deals where seller_inn = '921912462' and not is_cancelled"},
    {"q": "Сколько всего экспортных сделок и на какую сумму в долларах (без аннулированных)?",
     "sql": """select count(*) filter (where contract_type = 'Экспортный'),
                      sum(amount_usd) filter (where contract_type = 'Экспортный' and not is_cancelled)
               from deals"""},
    {"q": "2025-yilda necha tonna paxta xomashyosi sotilgan?",
     "sql": """select sum(volume_tonnes) from deals
               where year = 2025 and product = 'Хлопок-сырец' and not is_cancelled"""},
    {"q": "Какая доля сделок 2026 года исполнена частично?",
     "sql": """select 100.0 * count(*) filter (where status = 'Исполнен(Частично)') / count(*)
               from deals where year = 2026"""},
    {"q": "280092 raqamli bitim haqida ma’lumot ber",
     "sql": "select amount, qty_lots from deals where deal_id = 280092"},
    {"q": "30.10.2026 kuni dollar kursi qancha bo‘lgan?",
     "sql": "select rate from usd_rates where rate_date = date '2026-10-30'"},
    {"q": "Кто крупнейший покупатель по сумме сделок за всё время?",
     "sql": """select c.name from deals d join companies c on c.inn = d.buyer_inn where not is_cancelled
               group by 1 order by sum(amount_uzs) desc limit 1""", "text": True},
    {"q": "Qancha bitim to‘langan, lekin tovar hali yetkazilmagan?",
     "sql": "select count(*) from deals where status = 'Оплачен'"},
    {"q": "Какой средний срок оплаты в днях по исполненным сделкам?",
     "sql": """select avg(payment_date - deal_date) from deals
               where status in ('Исполнен', 'Исполнен(Частично)')"""},
    {"q": "2025-yilda qaysi oyda savdo aylanmasi eng yuqori bo‘lgan va qancha?",
     "sql": """select sum(amount_uzs) from deals where year = 2025 and not is_cancelled
               group by month order by 1 desc limit 1"""},
    {"q": "Сколько уникальных покупателей участвовало в торгах в 2023 году?",
     "sql": "select count(distinct buyer_inn) from deals where year = 2023"},
    {"q": "КАМЎЛИ ПЛУС kompaniyasi nechta bitim tuzgan?",
     "sql": "select count(*) from deals where buyer_inn = '903284941' or seller_inn = '903284941'"},
    {"q": "Сколько литров бензина АИ-92 продано в 2024 году?",
     "sql": """select sum(volume) from deals where year = 2024 and product = 'Бензин автомобильный'
               and mark = 'АИ-92' and unit = 'литр' and not is_cancelled"""},
    {"q": "Бухоро вилоятида 2022 йилда нечта битим тузилган?",
     "sql": "select count(*) from deals where year = 2022 and region_key = 'buxoro'"},
    {"q": "Obratniy auksion nima va nechta shunday bitim bo‘lgan?",
     "sql": "select count(*) from deals where trade_type = 'Обратный аукцион'"},
    {"q": "Salom! Nimalarni so‘rasam bo‘ladi?", "sql": None},
    {"q": "Какая завтра погода в Ташкенте?", "sql": None},
]
