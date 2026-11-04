"""UZEX SmartQuery API testlari.

    UZEX_URL=http://127.0.0.1:8000 .venv/bin/pytest api/uzex -v
    UZEX_URL=https://uzex-smartquery.vercel.app .venv/bin/pytest api/uzex -v

AI endpointi faqat tayyor (keshdagi) savollar va validatsiya bilan tekshiriladi — Gemini limiti sarflanmaydi.
"""
import os
import time

import pytest
import requests

BASE = os.getenv("UZEX_URL", "http://127.0.0.1:8000").rstrip("/")
S = requests.Session()


def get(path, **params):
    return S.get(BASE + path, params=params, timeout=60)


def ask(question, **extra):
    return S.post(BASE + "/api/v1/ask", json={"question": question, **extra}, timeout=120)


# ---------- sog'lik va statik ----------
def test_health_200_va_model_royxati():
    r = get("/api/health")
    assert r.status_code == 200
    d = r.json()
    assert d["ok"] is True and d["model"] and len(d["models"]) >= 2


@pytest.mark.parametrize("path,ctype", [("/", "text/html"), ("/styles.css", "text/css"), ("/app.js", "javascript"),
                                        ("/views.js", "javascript"), ("/assets/favicon.svg", "image/svg")])
def test_statik_fayllar_beriladi(path, ctype):
    r = get(path)
    assert r.status_code == 200 and ctype in r.headers["content-type"]


def test_yoq_sahifa_404():
    assert get("/yoq-sahifa-xyz").status_code == 404


def test_env_va_maxfiy_fayllar_berilmaydi():
    for p in ("/.env", "/../.env", "/%2e%2e/.env", "/app/agent.py", "/data/uzex.duckdb"):
        r = get(p)
        assert r.status_code in (400, 404), p
        assert "GEMINI_API_KEY" not in r.text


# ---------- stats ----------
def test_stats_raqamlari_datasetga_mos():
    d = get("/api/v1/stats").json()
    assert (d["deals"], d["contracts"], d["companies"], d["brokers"]) == (500000, 6616, 14392, 120)
    assert [y["deals"] for y in d["by_year"]] == [84299, 93985, 106647, 115763, 99306]
    assert d["last_date"] == "2026-10-30"
    assert sum(y["deals"] for y in d["by_year"]) == d["deals"]


# ---------- deals ----------
def test_deals_standart_sahifa():
    d = get("/api/v1/deals").json()
    assert d["total"] == 500000 and d["page"] == 1 and len(d["rows"]) == 25
    ids = [r["deal_id"] for r in d["rows"]]
    assert ids == sorted(ids, reverse=True)


def test_deals_filtrlar_birga():
    d = get("/api/v1/deals", year=2025, product="Карбамид", size=100).json()
    assert d["total"] > 0
    assert all(r["product"] == "Карбамид" and r["deal_date"].startswith("2025") for r in d["rows"])


def test_deals_bitim_raqami_va_stir_qidiruvi():
    d = get("/api/v1/deals", q="280092").json()
    assert d["total"] == 1 and d["rows"][0]["deal_id"] == 280092
    d = get("/api/v1/deals", q="903284941").json()
    assert d["total"] == 22


def test_deals_kirill_lotin_qidiruv_bir_xil():
    a = get("/api/v1/deals", q="kamoli plus").json()["total"]
    b = get("/api/v1/deals", q="КАМЎЛИ ПЛУС").json()["total"]
    assert a == b == 22


@pytest.mark.parametrize("params", [{"page": 0}, {"page": -5}, {"size": 0}, {"size": 100000}, {"page": 999999}])
def test_deals_pagination_chegaralari(params):
    r = get("/api/v1/deals", **params)
    assert r.status_code == 200
    d = r.json()
    assert 1 <= d["size"] <= 100 and d["page"] >= 1


@pytest.mark.parametrize("params", [{"year": "abc"}, {"page": "x"}, {"size": "1.5"}])
def test_deals_notogri_tur_422(params):
    assert get("/api/v1/deals", **params).status_code == 422


@pytest.mark.parametrize("payload", ["' OR 1=1 --", "'; DROP TABLE deals; --", "%' UNION SELECT 1 --", "\\'", "ʼ’‘"])
def test_deals_sql_injection_xavfsiz(payload):
    r = get("/api/v1/deals", q=payload)
    assert r.status_code == 200
    assert r.json()["total"] < 500000
    assert get("/api/v1/stats").json()["deals"] == 500000  # jadval joyida


def test_deals_injection_filtrlarda():
    r = get("/api/v1/deals", product="x' OR '1'='1", region="' OR 1=1 --", status="'")
    assert r.status_code == 200 and r.json()["total"] == 0


# ---------- products / participants / filters / sources ----------
def test_products_41_ta_va_ulushlar():
    rows = get("/api/v1/products").json()["rows"]
    assert len(rows) == 41
    assert rows[0]["product"] == "Хлопок-сырец"
    tv = [r["turnover_uzs"] or 0 for r in rows]
    assert tv == sorted(tv, reverse=True)


def test_products_yil_filtri():
    rows = get("/api/v1/products", year=2024).json()["rows"]
    carb = next(r for r in rows if r["product"] == "Карбамид")
    assert abs(carb["avg_price_uzs"] - 4762397.37) < 1


@pytest.mark.parametrize("role", ["buyer", "seller", "broker"])
def test_participants_rollar(role):
    rows = get("/api/v1/participants", role=role, limit=10).json()["rows"]
    assert 0 < len(rows) <= 10 and all(r["deals"] > 0 for r in rows)


def test_participants_qidiruv_stir():
    rows = get("/api/v1/participants", role="seller", q="921912462").json()["rows"]
    assert len(rows) == 1 and abs(rows[0]["turnover_uzs"] - 532671365716.03) < 1


def test_participants_noma_lum_rol_xaridor_deb_olinadi():
    r = get("/api/v1/participants", role="hacker")
    assert r.status_code == 200


@pytest.mark.parametrize("limit", [0, -1, 100000])
def test_participants_limit_chegaralari(limit):
    r = get("/api/v1/participants", limit=limit)
    assert r.status_code == 200 and 1 <= len(r.json()["rows"]) <= 200


def test_filters_va_sources():
    f = get("/api/v1/filters").json()
    assert f["years"] == [2022, 2023, 2024, 2025, 2026] and len(f["products"]) == 41 and len(f["regions"]) == 14
    s = get("/api/v1/sources").json()
    assert {t["table"] for t in s["tables"]} == {"deals", "contracts", "companies", "brokers", "usd_rates"}
    assert s["normalization"] == {"raw_names": 230, "products": 41, "specs": 92}


# ---------- ask (AI) ----------
def test_ask_tayyor_savol_tez_va_togri():
    t = time.time()
    r = ask("Datasetda qanday ma’lumotlar mavjud?")
    assert r.status_code == 200 and time.time() - t < 10
    d = r.json()
    assert d["status"] == "ok" and d["language"] == "uz" and "500 000" in d["answer"]
    assert d["conversation_id"] and d["source"]["sql"]


def test_ask_ruscha_tayyor_savol_ruscha_javob():
    d = ask("Топ-5 брокеров покупателя по числу сделок.").json()
    assert d["language"] == "ru" and "FIPI BROKER" in d["answer"] and "13 447" in d["answer"]
    assert d["visualization"]["type"] == "hbar" and len(d["visualization"]["labels"]) == 5


def test_ask_filtrlar_odam_tilida():
    d = ask("2025-yilda nechta bitim tuzilgan?").json()
    texts = [f["text"] for f in d["source"]["filters"]]
    assert "yil: 2025" in texts
    assert not any("select" in t.lower() for t in texts)


@pytest.mark.parametrize("body", [{}, {"question": ""}, {"question": "x" * 2001}, {"question": 123},
                                  {"question": "ok", "conversation_id": "x" * 65}])
def test_ask_validatsiya_422(body):
    r = S.post(BASE + "/api/v1/ask", json=body, timeout=30)
    assert r.status_code == 422


def test_ask_json_emas_422():
    r = S.post(BASE + "/api/v1/ask", data="salom", headers={"Content-Type": "text/plain"}, timeout=30)
    assert r.status_code == 422


def test_reset_ishlaydi():
    assert S.post(BASE + "/api/reset", json={"conversation_id": "test123"}, timeout=30).json() == {"ok": True}
    assert S.post(BASE + "/api/reset", json={}, timeout=30).status_code == 200


# ---------- telegram webhook himoyasi ----------
@pytest.mark.parametrize("headers", [{}, {"X-Telegram-Bot-Api-Secret-Token": "notogri"}])
def test_webhook_maxfiy_kalitsiz_403(headers):
    r = S.post(BASE + "/api/telegram/webhook", json={"update_id": 1}, headers=headers, timeout=30)
    assert r.status_code == 403


# ---------- tezlik ----------
@pytest.mark.parametrize("path", ["/api/v1/stats", "/api/v1/deals", "/api/v1/products", "/api/v1/participants",
                                  "/api/v1/filters"])
def test_javob_vaqti(path):
    get(path)  # isitish
    t = time.time()
    get(path)
    limit = 3.0 if "vercel" in BASE else 1.5
    assert time.time() - t < limit, f"{path} sekin"


@pytest.mark.parametrize("role", ["buyer", "seller", "broker"])
def test_participants_tinish_belgilari_hammasini_qaytarmaydi(role):
    rows = get("/api/v1/participants", role=role, q="''").json()["rows"]
    assert rows == []


def test_deals_juda_katta_page_500_bermaydi():  # fuzz topgan xato: page=2^63 -> 500
    r = get("/api/v1/deals", page=9223372036854775808)
    assert r.status_code in (200, 422)
    r = get("/api/v1/deals", page=99999999)
    assert r.status_code == 200 and r.json()["rows"] == []


@pytest.mark.parametrize("path", ["/api/v1/deals", "/api/v1/products", "/api/v1/participants"])
@pytest.mark.parametrize("year", [0, -1, 99999999999999999999])
def test_yil_chegaradan_tashqari_422(path, year):
    assert get(path, year=year).status_code == 422
