# Security

## Reporting a vulnerability

Email: **your@email.com** (or open a private security advisory on the repo). Please include:

- Affected version / commit
- Steps to reproduce
- Impact assessment (data exposure / privilege escalation / DoS / …)

We aim to acknowledge within 48h and ship a fix within 7 days for high-severity issues.

---

## Security model

### Authentication
- **JWT (`HS256`)** signed with `SECRET_KEY`. Access token TTL = `ACCESS_TOKEN_EXPIRE_MINUTES` (default 30 min). Refresh token TTL = `REFRESH_TOKEN_EXPIRE_MINUTES` (default 7 days).
- **Password hashing:** bcrypt via `passlib`. Plain passwords never persisted.
- **OAuth 2.0 (Google)** — auth-code flow. Token validated server-side, internal user record looked up/created by email.
- **Session management** — DB-backed sessions with revocation. Each refresh-token issuance creates a session row; `/sessions` endpoint lets users see + revoke devices.
- **Admin API key** — static `settings.API_KEY` matched via `X-API-Key` header for service-to-service calls. Constant-time compared with `secrets.compare_digest()`.

### Authorization

- **Role-based** via `RoleChecker` dep (`UserRole.USER` / `UserRole.ADMIN`).
- **Admin pages** require `role=admin`. Sensitive ops (impersonate user, system-health) gated separately.
- **Workspace scope** — every authenticated request resolves an `ActiveOrg` (default = personal org). Resources scoped by `organization_id` foreign key.
- **Org roles:** `OWNER` / `ADMIN` / `MEMBER`. Owner can transfer ownership + delete org.

### Transport / network

- **CORS** — origin list from `settings.CORS_ORIGINS`. Restrict to your domains in production.
- **HTTPS** — enforce via reverse proxy (Nginx / Traefik / ALB). Strict-Transport-Security header set in middleware when `ENVIRONMENT=production`.
- **CSP** — frontend sets `frame-ancestors 'none'` by default to prevent click-jacking. See `frontend/next.config.ts` headers block.

### Data

- **Secrets** — read from environment via `pydantic-settings`. Never committed. See `.env.example` + `ENV_VARS.md`.
- **Audit log** — admin-mutating actions (user updates, deletes, impersonations, role changes) recorded in `app_admin_audit_log` table with actor + IP + payload snapshot.
- **Stripe webhooks** — signature verified via `stripe.Webhook.construct_event(secret=STRIPE_WEBHOOK_SECRET)`. Idempotency table prevents replay.

### Hardening checklist for production

- [ ] Rotate `SECRET_KEY` and `API_KEY` from generated defaults.
- [ ] Set `DEBUG=false` and `ENVIRONMENT=production`.
- [ ] Restrict `CORS_ORIGINS` to your domain(s).
- [ ] Tune `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_PERIOD` in `.env`.
- [ ] Set `PROMETHEUS_AUTH_TOKEN` if `/metrics` is exposed on a public endpoint.
- [ ] Set `SENTRY_DSN` to ship errors. Verify PII scrubbing rules in `core/sentry.py`.
- [ ] Enforce HTTPS at the proxy layer.
- [ ] Run `pip-audit` / `bun audit` in CI for dependency vulnerabilities.
- [ ] Configure database backups + restore test schedule.
- [ ] Subscribe Stripe webhook to all relevant events; verify endpoint via Stripe CLI.

## Known limitations

- **No 2FA / MFA** out of the box. Plan to add TOTP via `pyotp` — see `notes/thingstofix.md` §A.13.
- **No SAML / OIDC** beyond Google OAuth. Enterprise SSO needs custom IdP integration.
- **No automatic PII redaction** in logs — be careful what you log.
