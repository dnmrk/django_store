# Architecture

## Overview

Django backend serving a REST API consumed by a React SPA frontend. The two are decoupled: Django handles data, auth, and business logic; React handles rendering and client-side state.

## Directory Structure

```
django_store/
├── store/              # Project config (settings.py, root urls.py, wsgi/asgi)
├── products/           # Product catalog app
│   ├── models.py       # Category, Product
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views + template views
│   ├── urls.py         # Template URL routes (namespace: products)
│   ├── api_urls.py     # /api/products/ routes
│   ├── admin.py        # Category + Product admin with slug auto-population
│   └── tests.py
├── cart/               # Cart management app
│   ├── api_urls.py     # /api/cart/ routes
│   └── tests.py
├── orders/             # Order processing app
│   ├── models.py       # Order, OrderItem
│   ├── api_urls.py     # /api/orders/ routes
│   └── tests.py
├── users/              # Authentication app
│   ├── api_urls.py     # /api/auth/ routes (JWT obtain/refresh/register)
│   ├── urls.py         # Template URL routes (namespace: users)
│   └── tests.py
├── frontend/           # React SPA (Vite)
│   └── src/
│       ├── api/        # Axios-based API client modules
│       ├── components/ # Reusable UI components
│       ├── context/    # AuthContext, CartContext
│       └── pages/      # Route-level components
└── media/              # Uploaded product images (development)
```

## URL Routing

Root `store/urls.py` routes:
- `/admin/` → Django admin
- `/api/products/` → `products.api_urls`
- `/api/cart/` → `cart.api_urls`
- `/api/orders/` → `orders.api_urls`
- `/api/auth/` → `users.api_urls` (JWT: obtain, refresh, register)
- `/cart/` → `cart.urls` (template views, namespace: cart)
- `/users/` → `users.urls` (template views, namespace: users)
- `/orders/` → `orders.urls` (template views, namespace: orders)
- `/` → `products.urls` (template views, namespace: products)

## Data Model

```
Category (name, slug)
  └── Product (category FK, name, slug, description, price, image, stock, available, created_at, updated_at)

Order (user FK, full_name, email, address, city, postal_code, status, created_at, updated_at)
  └── OrderItem (order FK, product FK, quantity, price)
```

## Authentication Flow

1. User POST `/api/auth/register/` → creates User account
2. User POST `/api/auth/token/` → returns `access` + `refresh` JWT tokens
3. Frontend stores tokens in localStorage, attaches `Authorization: Bearer <access>` via Axios interceptor
4. Protected API endpoints use DRF `IsAuthenticated` permission class
5. Token refresh via `/api/auth/token/refresh/`

## Patterns Used

- **Serializers as data contracts**: DRF serializers define the shape of API input/output
- **Class-based API views**: `APIView`, `generics.*`, or `ViewSet` for API endpoints
- **Template views**: Django template-rendered pages for server-side storefront (legacy; SPA is taking over)
- **JWT auth**: Stateless authentication — no session cookies for API
- **React Context**: Client-side auth state (`AuthContext`) and cart state (`CartContext`)
- **TanStack Query**: Server-state management and caching in the React frontend

## Key Constraints

- SQLite database — development only; production would require PostgreSQL
- Media files served by Django in development; would need CDN/S3 in production
- Frontend is a separate Vite dev server in development (port 5173); proxied or co-hosted in production
