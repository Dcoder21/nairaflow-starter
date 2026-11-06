"""NairaFlow worker (starter). Pulls queued transfers, runs the fraud check, moves the money."""
import json
import os
import time

import psycopg
import redis

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nairaflow:nairaflow@postgres:5432/nairaflow")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
FRAUD_RULE_V2 = os.getenv("FRAUD_RULE_V2", "false").lower() == "true"
LIMIT_KOBO = 5_000_000_00  # 5,000,000 naira


def fraud_check(amount_kobo: int) -> str | None:
    """Returns a block reason, or None if the transfer looks fine."""
    if amount_kobo > LIMIT_KOBO:
        return "amount above single-transfer limit"
    if FRAUD_RULE_V2 and amount_kobo % 8 == 0:
        # New "pattern" rule shipped in a hurry. Used in Project 2 as the bad release.
        return "suspicious amount pattern"
    return None


def process(conn, tid: str) -> None:
    with conn.transaction():
        row = conn.execute(
            "SELECT from_account, to_account, amount_kobo, status FROM transfers WHERE id = %s FOR UPDATE",
            (tid,),
        ).fetchone()
        if not row or row[3] != "PENDING":
            return
        src, dst, amount, _ = row
        reason = fraud_check(amount)
        if reason:
            conn.execute("UPDATE transfers SET status='BLOCKED', reason=%s WHERE id=%s", (reason, tid))
            return
        bal = conn.execute("SELECT balance_kobo FROM accounts WHERE id=%s FOR UPDATE", (src,)).fetchone()
        dest = conn.execute("SELECT id FROM accounts WHERE id=%s FOR UPDATE", (dst,)).fetchone()
        if not bal or not dest:
            conn.execute("UPDATE transfers SET status='FAILED', reason='unknown account' WHERE id=%s", (tid,))
            return
        if bal[0] < amount:
            conn.execute("UPDATE transfers SET status='FAILED', reason='insufficient funds' WHERE id=%s", (tid,))
            return
        conn.execute("UPDATE accounts SET balance_kobo = balance_kobo - %s WHERE id=%s", (amount, src))
        conn.execute("UPDATE accounts SET balance_kobo = balance_kobo + %s WHERE id=%s", (amount, dst))
        conn.execute("UPDATE transfers SET status='COMPLETED' WHERE id=%s", (tid,))


def main() -> None:
    queue = redis.Redis.from_url(REDIS_URL)
    print(f"worker started (FRAUD_RULE_V2={FRAUD_RULE_V2})", flush=True)
    while True:
        try:
            with psycopg.connect(DATABASE_URL) as conn:
                while True:
                    item = queue.brpop("transfers", timeout=5)
                    if item:
                        tid = json.loads(item[1])["id"]
                        process(conn, tid)
                        print(f"processed {tid}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"worker error: {exc}; retrying in 3s", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main()
