# django.henshuuz.dev deployment

This app is deployed by GitHub Actions after `main` is updated through the PR workflow.

## Architecture

- Nginx terminates public HTTP/HTTPS for `django.henshuuz.dev`.
- The React/Vite build is served from `/opt/django-store/current/frontend/dist`.
- `/api/` and `/admin/` are proxied to Gunicorn on `127.0.0.1:8010`.
- Django static and media files are served from `/var/www/django-store/static` and `/var/www/django-store/media`.
- Server-only secrets live in `/etc/django-store/django-store.env` and are not committed.

## GitHub Actions secrets

Required repository secrets:

- `SSH_HOST`
- `SSH_PORT`
- `SSH_USER`
- `SSH_KEY`

The deploy step uploads a release archive and runs the server helper:

```bash
sudo /usr/local/bin/deploy-django-store /tmp/django-store-release.tgz
```

## TLS

The tracked nginx config listens on port 80 only. The site MUST NOT serve real
traffic over plain HTTP — login credentials and JWTs would cross the wire in
cleartext. One-time provisioning on the server:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d django.henshuuz.dev   # obtains cert, adds 443 block + 80→443 redirect
```

Certbot edits `/etc/nginx/sites-available/django.henshuuz.dev` in place; re-deploys
copy the tracked config back, so after the first `certbot` run, fold its 443/redirect
changes into `deploy/nginx/django.henshuuz.dev.conf` and commit them.

After TLS works, keep `SECURE_SSL_REDIRECT=True` in the server env (the env example
defaults to it). Django then also sends HSTS headers (configured in `settings.py`
when `DEBUG=False`).

## Server files

Tracked templates live under `deploy/`:

- `deploy/bin/deploy-django-store` to `/usr/local/bin/deploy-django-store`
- `deploy/systemd/django-store.service` to `/etc/systemd/system/django-store.service`
- `deploy/nginx/django.henshuuz.dev.conf` to `/etc/nginx/sites-available/django.henshuuz.dev`
- `deploy/env/django-store.env.example` as the example for `/etc/django-store/django-store.env`
