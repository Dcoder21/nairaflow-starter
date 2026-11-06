from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_rejects_negative_amount():
    r = client.post("/transfers", json={"from_account": "ACC001", "to_account": "ACC002", "amount_kobo": -5})
    assert r.status_code == 422


def test_rejects_same_account():
    r = client.post("/transfers", json={"from_account": "ACC001", "to_account": "ACC001", "amount_kobo": 500})
    assert r.status_code == 400
