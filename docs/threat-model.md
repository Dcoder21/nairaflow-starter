# NairaFlow threat model (STRIDE)

Date: <today>  ·  Author: <your name>  ·  Scope: nairaflow-starter as it runs today (Docker Compose, manual deploys)

## What we are protecting

| Asset | Why it matters |
| --- | --- |
| Customer money (account balances, transfers) | Direct financial loss |
| Merchant KYC data | NDPA breach, partner bank escalation |
| Credentials (DB password, registry and cloud keys) | Lead to everything else |
| The build and deploy process | If it is compromised, attackers ship their own code |

## Threats

STRIDE = Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.

| # | STRIDE | Threat (what could go wrong) | Where | Linked incident | Control we will add | Day |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Information disclosure | Attacker on public Wi-Fi reads login tokens because the API accepts plain HTTP | web/api traffic | 4 (intercepted mobile traffic) | HTTPS only, HSTS, SSL pinning | 12–14 |
| 2 | Spoofing | | | | | |
| 3 | Tampering | | | | | |
| 4 | Repudiation | | | | | |
| 5 | Information disclosure | | | | | |
| 6 | Denial of service | | | | | |
| 7 | Elevation of privilege | | | | | |

Add at least 8 rows. Every row must link to a control in Project 1, or say why it is out of scope.

## Top 3 risks (in plain words)

1.
2.
3.
