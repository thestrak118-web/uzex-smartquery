# Birja bitimlari AI-agenti

Tovar-xomashyo birjasi bitimlari reyestri bo‘yicha savollarga **o‘zbek (lotin/kirill) va rus tillarida** javob beradigan agent.
Ikkita interfeysi bor: **Telegram-bot** va **veb-dashboard «UZEX SmartQuery»**. Ikkalasi bitta agent yadrosidan foydalanadi.

Veb-interfeys (`app/static`, dizayn — `design/uzex-smartquery-ui`): dataset ko‘rsatkichlari va yillik grafik
bazadan jonli olinadi; har bir javob ostida manba jadvallari, filtrlar, SQL, natija jadvali va avtomatik grafik
ko‘rsatiladi; so‘nggi so‘rovlar tarixi saqlanadi.

## Qanday ishlaydi

```
savol ─► Gemini (function calling) ─► run_sql / find_entity ─► DuckDB (500 000 bitim)
                ▲                                                    │
                └────────────── natija (jadval) ◄────────────────────┘
      ─► javob foydalanuvchi tilida
```

- `prepare.py` CSV fayllarni `data/uzex.duckdb` bazasiga yuklaydi va ma’lumotni tozalaydi:
  - **tovar nomlari**: 230 xil yozuv 41 ta kanonik tovarga keltirildi («Хлопок-сырец (спот)», «ХЛОПОК СЫРЕЦ (СПОТ)» → `Хлопок-сырец`; «Мочевина (карбамид)» → `Карбамид`);
  - **nav, sinf, marka**: «1-сорта», «I сорт», «первый сорт» → `1`; «ЦЕМ I 42,5Н» → `ЦЕМ I 42,5 Н`; atributlar faqat nomda yozilgan bo‘lsa, o‘sha yerdan ajratib olinadi;
  - **summalar**: eksport (USD) bitimlari bitim kunidagi kurs bo‘yicha so‘mga o‘girilgan (`amount_uzs`, `amount_usd`);
  - hisoblangan ustunlar: hajm (`volume = Количество × Лот`), tonnadagi hajm, birlik narxi;
  - kompaniya qidiruvi uchun kalit (kirill → lotin), masalan «КАМЎЛИ ПЛУС» = «kamoli plus».
- Agent faqat **o‘qish rejimida** SQL bajaradi: fayl tizimiga kirish yopiq, faqat `SELECT`, so‘rovga 20 soniya chegara.
- Hisoblash qoidalari tizim promptida yozilgan: bekor qilingan bitimlar aylanmaga kirmaydi, o‘rtacha narx vaznli hisoblanadi, so‘m va dollar bir-biriga qo‘shilmaydi, turli o‘lchov birliklari aralashtirilmaydi (benzin tonna va litrda sotilgan).

## O‘rnatish

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python prepare.py            # dataset/uzex_spot_data.zip ni ochadi va data/uzex.duckdb quradi (~3 s)
cp .env.example .env                   # GEMINI_API_KEY va TELEGRAM_BOT_TOKEN ni yozing
```

## Ishga tushirish

```bash
.venv/bin/python main.py               # veb (http://localhost:8000) + Telegram-bot
.venv/bin/python main.py --web         # faqat veb
.venv/bin/python main.py --bot         # faqat bot
.venv/bin/python main.py --ask "2025-yilda nechta bitim tuzilgan?"
.venv/bin/python main.py --models      # kalit bilan mavjud Gemini modellari
.venv/bin/python -m eval.run_eval      # 24 ta test savol, to‘g‘ri javob bilan solishtirish
```

## Vercel'ga deploy

1. Vercel'da GitHub repo'ni import qiling (framework: FastAPI, entrypoint — `main.py` dagi `app`).
2. **Settings → Environment Variables** ga qo‘shing: `GEMINI_API_KEY` (majburiy), ixtiyoriy `GEMINI_MODEL`,
   `GEMINI_FALLBACKS`. So‘ng **Redeploy** qiling.
3. Baza alohida yuklanmaydi: birinchi so‘rovda `dataset/uzex_spot_data.zip` dan `/tmp/uzex.duckdb` ga ~2–5 s da quriladi.

Telegram-bot serverless'da polling bilan ishlay olmaydi. Uni Vercel'ga ko‘chirish uchun Vercel'ga
`TELEGRAM_BOT_TOKEN` va `TELEGRAM_WEBHOOK_SECRET` (istalgan uzun tasodifiy satr) qo‘shing, keyin lokalda:
`python main.py --set-webhook https://<sizning-domen>.vercel.app`. Lokal polling'ga qaytish: `python main.py --delete-webhook`.

## API

- `POST /api/v1/ask` — `{"question", "language": "uz|ru", "conversation_id"}` →
  `{"answer", "status": "ok|no_data|busy|error", "language", "conversation_id", "source": {tables, filters, sql, model, steps, seconds}, "visualization": {type, title, labels, values}, "table"}`
- `GET /api/v1/stats` — dashboard ko‘rsatkichlari, `POST /api/reset` — suhbatni tozalash, `GET /api/docs` — Swagger

## Telegram-bot buyruqlari

- `/start` — salomlashish va misol savollar
- `/new` — yangi suhbat (kontekstni tozalash)
- `/sql` — oxirgi javob uchun ishlatilgan SQL
- Javob ostidagi **🧾 SQL** va **📊 CSV** tugmalari — so‘rovni ko‘rish va natijani Excel uchun yuklab olish

## Misol savollar

- 2025-yilda eng ko‘p savdo qilingan 5 ta tovar qaysi?
- 2024-yilda karbamidning 1 tonnasi o‘rtacha qanchadan sotilgan?
- Какой брокер покупателя заключил больше всего сделок?
- КАМЎЛИ ПЛУС компанияси нечта битим тузган?
- 280092 raqamli bitim haqida ma’lumot ber

## Fayllar

| Fayl | Vazifasi |
|---|---|
| `prepare.py` | CSV → DuckDB, tozalash va normallashtirish |
| `app/normalize.py` | tovar lug‘ati, nav/sinf/marka qoidalari, kirill→lotin |
| `app/db.py` | xavfsiz SQL bajarish, kompaniya/broker qidiruvi |
| `app/prompt.py` | tizim prompti: sxema, katalog, hisoblash qoidalari, javob uslubi |
| `app/agent.py` | Gemini bilan agent sikli, suhbat tarixi |
| `app/web.py`, `app/static/` | veb-servis (API v1) va UZEX SmartQuery interfeysi |
| `app/bot.py` | Telegram-bot (aiogram 3) |
| `eval/` | test savollar va avtomatik tekshiruv |
| `run.sh` | fonda ishga tushirish: `start / stop / restart / status / log` |
