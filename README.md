# NairaFlow Starter

Starter app for the Amdari DevOps cohort. NairaFlow is a fictional Lagos fintech: merchants send naira transfers, a worker runs a fraud check and moves the money.

It runs, but it is **not production-ready on purpose**. Turning it into a secure, observable, self-service platform is the cohort's work across Projects 1–3.

## Architecture

```
browser ──> web (nginx :8080) ──/api/──> api (FastAPI :8000) ──> Postgres
                                              │
                                              └── Redis queue ──> worker ──> Postgres
```

| Service | What it does | Port |
| --- | --- | --- |
| `web` | Merchant dashboard (static HTML behind nginx) | 8080 |
| `api` | REST API: accounts, create and read transfers | 8000 |
| `worker` | Pulls transfers off Redis, runs the fraud check, moves money | – |
| `postgres` | Accounts and transfers (seeded with 4 merchants) | 5432 (internal) |
| `redis` | Transfer queue | 6379 (internal) |

## Run it

Needs Docker Desktop (or Docker Engine + Compose v2).

```bash
cp .env.example .env
docker compose up --build
```

- Dashboard: http://localhost:8080
- API docs: http://localhost:8000/docs

Try a transfer:

```bash
curl -X POST localhost:8000/transfers -H 'Content-Type: application/json' \
  -d '{"from_account":"ACC001","to_account":"ACC002","amount_kobo":150000}'
curl localhost:8000/transfers
```

Run the unit tests:

```bash
cd services/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Reset everything: `docker compose down -v`

## API

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/healthz` | Liveness |
| GET | `/readyz` | Readiness (checks Postgres and Redis) |
| GET | `/accounts` | Balances in kobo (100 kobo = ₦1) |
| POST | `/transfers` | Returns 202 and queues the transfer |
| GET | `/transfers` | Last 20 transfers |
| GET | `/transfers/{id}` | Status: PENDING, COMPLETED, FAILED or BLOCKED |

## What is missing on purpose

| Gap | Fixed in |
| --- | --- |
| Naive Dockerfiles (full Python image, root user, no digest pin) | Project 1, Phase B |
| No CI pipeline, scanning, SBOM or signing | Project 1, Phase B |
| No Kubernetes manifests, Helm chart or Argo CD app | Project 1, Phase C |
| No infrastructure code | Project 1, Phase A |
| Plain HTTP, no TLS, no HSTS | Project 1, Phase C |
| Passwords in `docker-compose.yml` and `.env` | Project 1 (and Vault in Project 3) |
| No metrics, traces or structured logs | Project 2, Phase A |
| No health-based rollout or feature flags | Project 2, Phase B |
| No catalog entry, template or cost tags | Project 3 |

See `TASKS.md` for the checklist.

## Feature switches (for mentors)

| Variable | Effect | Used in |
| --- | --- | --- |
| `SLOW_MODE=true` | Adds 0.5–2 s delay to `POST /transfers` | Project 2: the salary-day slowdown to find with traces |
| `FRAUD_RULE_V2=true` | Turns on a buggy fraud rule that blocks about 12% of genuine transfers | Project 2: the bad release a canary must catch |

Load test (needs [k6](https://k6.io)): `k6 run loadtest/salary-day.js`
