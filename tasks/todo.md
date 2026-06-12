# Security Hardening PR — fix/security-hardening

Scope: critical + high code-side findings from the 2026-06-12 project review.
Deferred (follow-ups, not this PR): git-history purge of leaked DB artifacts (destructive,
needs explicit go), server TLS provisioning (ops), CartContext → TanStack Query migration,
API pagination + frontend pagination, stock reservation at checkout (design decision).

## Tasks

- [x] Untrack `django_store_db` and `datadump.json` (`git rm --cached`), extend `.gitignore`
- [x] `store/settings.py`: DEBUG defaults False; SECRET_KEY required when DEBUG=False (fail closed)
- [x] `store/settings.py`: prod security headers (HSTS + preload, nosniff, referrer policy) gated on `not DEBUG`; HttpOnly session/CSRF cookies
- [x] `store/settings.py`: DRF ScopedRateThrottle + `auth` rate for login/register
- [x] `users`: throttled `LoginView`, throttle on register, `LogoutView` blacklisting refresh token + route
- [x] `cart/serializers.py`: bound quantity (1–99)
- [x] `cart/cart.py`: Decimal money math (no float)
- [x] `orders/api_views.py`: `transaction.atomic` around order creation; price from current DB product price; skip deleted products; `prefetch_related` on list/detail views
- [x] `frontend/src/context/AuthContext.tsx`: call `/auth/logout/` to revoke refresh token on logout
- [x] `deploy/env/django-store.env.example` + `deploy/README.md`: SSL redirect default True with TLS caveat, SECRET_KEY generation hint, certbot runbook
- [x] Tests: orders (current price, auth required, empty cart, ownership, rollback on invalid data), cart (quantity bounds, decimal totals), users (logout revocation, login throttle)
- [x] Run `python manage.py test --parallel` + `npm run lint` + `npm run build` — green
- [x] Commit, push, open PR

## Review

**Files touched**: `.gitignore`, `store/settings.py`, `users/api_views.py`, `users/api_urls.py`,
`users/tests.py`, `cart/serializers.py`, `cart/cart.py`, `cart/tests.py`, `orders/api_views.py`,
`orders/tests.py`, `frontend/src/context/AuthContext.tsx`,
`deploy/env/django-store.env.example`, `deploy/README.md`; untracked `django_store_db`, `datadump.json`.

**Commands run**: `python manage.py test --parallel` (15 tests, OK), `python manage.py check`
(no issues), `cd frontend && npm run lint` (clean), `npm run build` (succeeds; pre-existing
chunk-size warning — code-splitting is a deferred follow-up).

**Verification notes**:
- CI exports `SECRET_KEY` and `DEBUG=True`, local `.env` has both → fail-closed settings break neither.
- Unauthenticated DRF responses are 403 (SessionAuthentication is the first authenticator, no
  WWW-Authenticate challenge) — tests assert 401-or-403.
- `SimpleRateThrottle.THROTTLE_RATES` snapshots settings at import; throttle test patches the
  class attribute instead of `override_settings`.
- Cart API response shape unchanged (FloatField serialization) — frontend unaffected.

**Lessons**: none from corrections this session.
