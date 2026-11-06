"""NairaFlow payments API (starter). Accepts transfers and queues them for the worker."""
import json
import os
import random
import time
import uuid

import psycopg
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nairaflow:nairaflow@postgres:5432/nairaflow")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
SLOW_MODE = os.getenv("SLOW_MODE", "false").lower() == "true"  # simulates salary-day slowness

app = FastAPI(title="NairaFlow API", version="0.1.0")
queue = redis.Redis.from_url(REDIS_URL)


def db():
    return psycopg.connect(DATABASE_URL, autocommit=True)


class TransferIn(BaseModel):
    from_account: str
    to_account: str
    amount_kobo: int = Field(gt=0, description="Amount in kobo (100 kobo = 1 naira)")
    narration: str = ""


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        queue.ping()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"not ready: {exc}")
    return {"status": "ready"}


@app.get("/accounts")
def list_accounts():
    with db() as conn:
        rows = conn.execute("SELECT id, owner, balance_kobo FROM accounts ORDER BY id").fetchall()
    return [{"id": r[0], "owner": r[1], "balance_kobo": r[2]} for r in rows]


@app.post("/transfers", status_code=202)
def create_transfer(t: TransferIn):
    if t.from_account == t.to_account:
        raise HTTPException(status_code=400, detail="cannot transfer to the same account")
    if SLOW_MODE:
        time.sleep(random.uniform(0.5, 2.0))
    tid = str(uuid.uuid4())
    with db() as conn:
        conn.execute(
            "INSERT INTO transfers (id, from_account, to_account, amount_kobo, narration, status) "
            "VALUES (%s, %s, %s, %s, %s, 'PENDING')",
            (tid, t.from_account, t.to_account, t.amount_kobo, t.narration),
        )
    queue.lpush("transfers", json.dumps({"id": tid}))
    return {"id": tid, "status": "PENDING"}


@app.get("/transfers")
def recent_transfers():
    with db() as conn:
        rows = conn.execute(
            "SELECT id, from_account, to_account, amount_kobo, status, reason, created_at "
            "FROM transfers ORDER BY created_at DESC LIMIT 20"
        ).fetchall()
    keys = ["id", "from_account", "to_account", "amount_kobo", "status", "reason", "created_at"]
    return [dict(zip(keys, r)) for r in rows]


@app.get("/transfers/{tid}")
def get_transfer(tid: str):
    with db() as conn:
        row = conn.execute("SELECT id, status, reason FROM transfers WHERE id = %s", (tid,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="transfer not found")
    return {"id": row[0], "status": row[1], "reason": row[2]}
