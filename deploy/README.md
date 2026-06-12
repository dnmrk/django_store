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

## Server files

Tracked templates live under `deploy/`:

- `deploy/bin/deploy-django-store` to `/usr/local/bin/deploy-django-store`
- `deploy/systemd/django-store.service` to `/etc/systemd/system/django-store.service`
- `deploy/nginx/django.henshuuz.dev.conf` to `/etc/nginx/sites-available/django.henshuuz.dev`
- `deploy/env/django-store.env.example` as the example for `/etc/django-store/django-store.env`
