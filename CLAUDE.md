# Django Store

Full-stack e-commerce app — Django 4.2 REST API backend + React 19 SPA frontend with JWT auth, product catalog, cart, and orders.

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework 3.16, djangorestframework-simplejwt 5.5
- **Language**: Python 3.9
- **Frontend**: React 19, Vite 8, React Router 7, TanStack Query 5, Bootstrap 5
- **Database**: SQLite (dev only)
- **Testing**: Django built-in test runner
- **Linting**: ESLint (frontend)

## Setup

```bash
# Backend
source venv/bin/activate

# Frontend
cd frontend && npm install
```

## Commands

```bash
# Run backend dev server
python manage.py runserver

# Run frontend dev server
cd frontend && npm run dev

# Run tests (parallel — default)
python manage.py test --parallel

# Run tests (sequential — for debugging)
python manage.py test

# Run specific app tests
python manage.py test products

# Lint frontend
cd frontend && npm run lint

# Migrations
python manage.py makemigrations && python manage.py migrate
```

## Project Structure

- `store/` — Project config (settings, root URLs)
- `products/` — Product catalog (Category, Product models + API)
- `cart/` — Cart management (session + API)
- `orders/` — Order processing (Order, OrderItem models + API)
- `users/` — Auth (JWT register/login endpoints)
- `frontend/src/` — React SPA (api/, components/, context/, pages/)

## Key Rules

- Activate `venv` before all Python/Django commands
- API URL files are named `api_urls.py`; template URL files are `urls.py`
- Use `APITestCase` from `rest_framework.test` for API tests
- Use `select_related`/`prefetch_related` to avoid N+1 queries
- JWT tokens in localStorage; injected via Axios interceptor in `frontend/src/api/axios.js`
- TanStack Query for all server state in React — no raw `useEffect` data fetching
- New API endpoints need both the view and a route in `api_urls.py`

## Detailed Configuration

Project configuration files are in `.claude/`:
- `project-overview.md` — Project identity and philosophy
- `architecture.md` — Technical patterns and structure
- `testing.md` — Test configuration and commands
- `code-standards.md` — Coding conventions
- `pipeline.md` — Autonomous development workflow agents
