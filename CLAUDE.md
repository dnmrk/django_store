# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Activate the virtual environment before running any commands:

```bash
source venv/bin/activate
```

## Commands

```bash
# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Run a specific test
python manage.py test products.tests.MyTestCase

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Create superuser (for admin access)
python manage.py createsuperuser
```

## Architecture

This is a Django 4.2 e-commerce store project. The Django project config lives in `store/` (settings, root URLs, wsgi/asgi). All product domain logic lives in the `products/` app.

**Data model:** `Category` has many `Product`s (FK with CASCADE). Products have `available`/`stock` fields that control storefront visibility. Product images upload to `media/products/` and are served via `MEDIA_URL` in development.

**URL routing:** Root URLs (`store/urls.py`) delegate everything except `/admin/` to `products.urls` (namespace `products`). Two views: `product_list` (homepage, filters `available=True`) and `product_detail` (slug lookup).

**Templates:** All templates live under `products/templates/products/` and extend `base.html`, which loads Bootstrap 5 from CDN.

**Database:** SQLite (`db.sqlite3`) — development only.

**Admin:** Both `Category` and `Product` are registered with slug auto-population from name.
