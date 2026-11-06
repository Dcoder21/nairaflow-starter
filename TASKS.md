# Cohort checklist

## Project 1: Secure delivery
- [ ] Push this repo to the cohort's self-managed GitLab
- [ ] Phase A: OpenTofu modules, remote state, merge request pipeline, 5 OPA/Conftest policies
- [ ] Phase B: harden all 3 Dockerfiles (multi-stage, slim or distroless, non-root, digest-pinned)
- [ ] Phase B: `.gitlab-ci.yml` — lint, test, Gitleaks, Semgrep, build, Trivy, Syft SBOM, Cosign sign, push to Harbor
- [ ] Phase C: Helm chart or Kustomize overlays (dev, staging, prod) + Argo CD app
- [ ] Phase C: Kyverno policies (signed images only, no `latest`, no root)
- [ ] Phase C: HTTPS with cert-manager + Gateway API, TLS 1.2/1.3, HSTS, mTLS between services
- [ ] Phase C: SSL pinning demo + pin rotation runbook
- [ ] Rollback with `git revert` in under 5 minutes

## Project 2: Reliable operations
- [ ] OpenTelemetry in `api` and `worker` (2 custom spans on the transfer path)
- [ ] Prometheus, Loki, Tempo, Grafana dashboard as code
- [ ] 2 SLOs + burn-rate alerts + runbooks
- [ ] Find the `SLOW_MODE` bottleneck with k6 + traces
- [ ] Argo Rollouts canary that auto-aborts when `FRAUD_RULE_V2=true` ships
- [ ] Move `FRAUD_RULE_V2` behind an OpenFeature flag
- [ ] 3 Chaos Mesh experiments, game day, blameless postmortem

## Project 3: Capstone
- [ ] Backstage catalog entry (`catalog-info.yaml`) for each service
- [ ] Golden-path template that creates a new service like this one
- [ ] Crossplane claim for Postgres; secrets from Vault via External Secrets
- [ ] Requests/limits, HPA or KEDA, OpenCost report per team
