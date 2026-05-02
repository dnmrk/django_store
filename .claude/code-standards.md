# Code Standards

## Style Guide
- **Backend**: PEP 8 (Python standard)
- **Frontend**: Airbnb-style via ESLint (configured in `frontend/eslint.config.js`)

## Linting

```bash
# Backend — no linter installed; follow PEP 8 manually
# To add ruff (recommended): pip install ruff && ruff check .

# Frontend — check for issues
cd frontend && npm run lint

# Frontend — ESLint does not auto-fix by default; add --fix to fix safe issues
cd frontend && npx eslint . --fix
```

## Formatting
```bash
# Frontend (Vite/ESLint handles this)
cd frontend && npm run lint
```

## Pre-commit Checks
- Backend: All Django tests must pass (`python manage.py test --parallel`)
- Frontend: ESLint must pass (`cd frontend && npm run lint`)

## Naming Conventions

### Python / Django
- Classes: `PascalCase` (e.g., `ProductSerializer`, `OrderDetailView`)
- Functions/methods: `snake_case` (e.g., `get_queryset`, `calculate_total`)
- Variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- URL names: `snake_case` (e.g., `product_list`, `order_detail`)
- Model fields: `snake_case`
- Files/modules: `snake_case` (e.g., `api_urls.py`, `serializers.py`)

### React / JavaScript
- Components: `PascalCase` (e.g., `ProductCard`, `Navbar`)
- Hooks: `camelCase` prefixed with `use` (e.g., `useProducts`, `useAuth`)
- Variables/functions: `camelCase`
- Files: `PascalCase` for components (e.g., `ProductDetailPage.jsx`), `camelCase` for utils/api

## Django-Specific Rules
- Serializers live in `{app}/serializers.py`
- API URL routing lives in `{app}/api_urls.py` (separate from template URLs in `{app}/urls.py`)
- Views for the API live in `{app}/views.py` (class-based where appropriate)
- One model file per app (`{app}/models.py`); split into `models/` package only if >200 lines
- Always use `related_name` on FK/M2M fields
- Use `select_related` / `prefetch_related` to avoid N+1 queries

## React-Specific Rules
- API calls live in `src/api/{resource}.js` (e.g., `src/api/products.js`)
- Shared state via React Context in `src/context/`
- Pages (route-level components) in `src/pages/`
- Reusable components in `src/components/`
- Use TanStack Query for all server state; avoid manual fetch/useEffect patterns
- JWT tokens stored in localStorage, injected via Axios interceptors in `src/api/axios.js`
