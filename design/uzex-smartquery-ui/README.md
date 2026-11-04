# UZEX SmartQuery — UI prototype

UZEX AI Hackathon saralash topshirig‘i uchun birja bitimlari bo‘yicha savol-javob AI agentining frontend dizayn prototipi.

## Ishga tushirish

1. ZIP arxivni oching.
2. `index.html` faylini Chrome yoki Firefox brauzerida oching.
3. Internet aloqasi bo‘lsa Google Fonts yuklanadi; internet bo‘lmasa tizim shriftlari ishlatiladi.

Node.js, npm yoki build jarayoni talab qilinmaydi.

## Hozirgi imkoniyatlar

- Responsive dashboard (desktop, tablet, mobile).
- O‘zbekcha / ruscha interfeys almashinuvi.
- Dataset ko‘rsatkichlari va yillar kesimidagi bitimlar grafigi.
- AI chat interfeysi va tezkor savol namunalari.
- Demo javoblar: 2025-yil bitimlar soni, yillik dinamika va dataset tarkibi.
- So‘nggi savollar ro‘yxati.

## Muhim: demo va haqiqiy backend farqi

Bu ZIP — frontend/UI prototipi. Hozircha haqiqiy LLM, DuckDB yoki FastAPI backend ulanmagan. Chatdagi uchta javob README ma’lumotlaridan olingan oldindan tayyorlangan demo javoblardir. Boshqa savollarda tizim backend ulanmaganini bildiradi; uydirma javob bermaydi.

Dataset README fayliga ko‘ra, barcha kompaniya, STIR, bitim, narx va kurs yozuvlari sun’iy (synthetic). UI real UZEX ma’lumotlari sifatida taqdim etilmasligi kerak.

## Backend ulash uchun tavsiya etilgan API

`POST /api/v1/ask`

Request:

```json
{
  "question": "2025-yilda nechta bitim tuzilgan?",
  "language": "uz",
  "conversation_id": null
}
```

Response:

```json
{
  "answer": "2025-yil uchun datasetda 115 763 ta bitim qayd etilgan.",
  "status": "ok",
  "language": "uz",
  "source": {
    "tables": ["deals_2025"],
    "filters": {"year": 2025},
    "metric": "deal_count"
  },
  "visualization": null
}
```

Frontend integratsiyasida `app.js` ichidagi `sendQuestion()` funksiyasi `fetch('/api/v1/ask', ...)` bilan almashtiriladi. Backend SQL so‘rovlarni oldindan belgilangan va tekshirilgan query funksiyalari orqali bajarishi kerak; LLM'ga cheklanmagan SQL bajarish huquqi berilmasin.

## Dataset snapshot

| Ko‘rsatkich | Qiymat |
|---|---:|
| Bitimlar | 500,000 |
| Shartnoma kartochkalari | 6,616 |
| Ishtirokchilar | 14,392 |
| Brokerlar | 120 |

Yillar kesimida:

| Yil | Bitimlar |
|---|---:|
| 2022 | 84,299 |
| 2023 | 93,985 |
| 2024 | 106,647 |
| 2025 | 115,763 |
| 2026 (30-oktabrgacha) | 99,306 |

Ushbu qiymatlar berilgan datasetning README faylidan olingan.
