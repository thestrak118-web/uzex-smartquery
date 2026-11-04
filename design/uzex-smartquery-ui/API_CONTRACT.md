# Backend integration contract

## Endpoint

`POST /api/v1/ask`

## Request body

```json
{
  "question": "...",
  "language": "uz | ru",
  "conversation_id": "optional-string"
}
```

## Successful response

```json
{
  "answer": "...",
  "status": "ok",
  "language": "uz",
  "source": {
    "tables": ["deals_2025"],
    "filters": {"year": 2025},
    "metric": "deal_count"
  },
  "visualization": {
    "type": "bar",
    "title": "Bitimlar soni",
    "labels": ["2022", "2023", "2024", "2025", "2026"],
    "values": [84299, 93985, 106647, 115763, 99306]
  }
}
```

## No-data response

```json
{
  "answer": "So‘rov bo‘yicha datasetda ma’lumot topilmadi.",
  "status": "no_data",
  "language": "uz",
  "source": null,
  "visualization": null
}
```

## Safety and correctness requirements

- Do not invent missing facts or values.
- Return applied date range, filters, metric, and source tables.
- Run aggregation in DuckDB/SQL, not in free-form LLM text generation.
- Validate query plans and use allow-listed query templates or safe parameterized SQL.
- Respect the synthetic nature of the provided dataset.
- Treat 2026 as a partial year through 30 October 2026.
