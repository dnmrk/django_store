# Repository Guidelines

## Project Structure & Module Organization

This is a full-stack Django Store application. Django project configuration lives in `store/`, with feature apps in `products/`, `cart/`, `orders/`, `users/`, and `forecasting/`. Apps keep models, views, serializers, URL modules, migrations, and tests together; API routes use `api_urls.py`, while template routes use `urls.py`. Shared templates are in `templates/`, app templates are under each app's `templates/`, uploaded media is in `media/`, and the React/Vite SPA is in `frontend/src/`. The optional Shiny analytics service is in `analytics/`; deployment assets are in `Dockerfile`, `docker-compose*.yml`, and `nginx/`.

## Build, Test, and Development Commands

- `source venv/bin/activate`: activate the Python environment.
- `pip install -r requirements.txt`: install backend dependencies.
- `python manage.py migrate`: apply database migrations.
- `python manage.py runserver`: run the Django backend at `http://127.0.0.1:8000`.
- `python manage.py test --parallel`: run backend tests.
- `cd frontend && npm install`: install frontend dependencies.
- `cd frontend && npm run dev`: run Vite locally.
- `cd frontend && npm run build`: build production frontend assets.
- `cd frontend && npm run lint`: run ESLint for frontend code.
- `docker compose -f docker-compose.dev.yml up --build`: run PostgreSQL, Django, and analytics services together.

## Coding Style & Naming Conventions

Use 4-space indentation for Python and follow Django conventions: `snake_case` for functions, variables, and modules; `PascalCase` for models, forms, serializers, and class-based views. Keep app-specific logic inside the relevant app. React code uses TypeScript/TSX, `PascalCase` component files such as `ProductDetailPage.tsx`, and camelCase functions and variables. Prefer TanStack Query for server state and existing Axios clients in `frontend/src/api/`.

## Testing Guidelines

Backend tests use Django's test runner; place tests in each app's `tests.py` or a local `tests/` package if the suite grows. Name methods `test_<behavior>`, and use `rest_framework.test.APITestCase` for API endpoints. Cover model behavior, permissions, serializers, and endpoint responses when backend behavior changes. There is no configured frontend test runner; run `npm run lint` and `npm run build` after frontend changes.

## Commit & Pull Request Guidelines

Recent commits use short, title-case summaries such as `TypeScript Migration` and `Sales Forecasting Feature`. Keep commits focused and user-facing. Pull requests should include a concise summary, test results, linked issues when applicable, migration notes for model changes, and screenshots for visible UI changes.

## Security & Configuration Tips

Keep secrets in `.env`; do not commit real credentials, database dumps, or generated media. Review `store/settings.py` when changing CORS, JWT, static files, or embedded analytics settings.
