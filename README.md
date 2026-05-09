# Django Store

A full-stack e-commerce application built with Django, Django REST Framework, React (TypeScript), and a Shiny for Python analytics dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.x + Django REST Framework |
| Auth | Simple JWT |
| Frontend | React 18 + TypeScript + Vite |
| Styling | Bootstrap 5 |
| Data fetching | TanStack Query + Axios |
| Analytics | Shiny for Python + Plotly |
| ML / Forecasting | pandas + scikit-learn + numpy |
| Database | SQLite (development) |

# Install dependencies
pip install django pillow

# Add to the Django dependencies list
pip install psycopg2-binary python-dotenv

# Apply migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The store will be available at `http://127.0.0.1:8000` and the admin at `http://127.0.0.1:8000/admin`.

## Adding Products

Use the Django admin to create categories and products. Product images are stored in `media/products/`.

## Project Structure

```
django_store/
├── store/                  ← Django project config & settings
├── products/               ← Product catalog app
├── users/                  ← Authentication app
├── cart/                   ← Session-based cart app
├── orders/                 ← Checkout & order history app
├── forecasting/            ← ML sales forecasting app
├── analytics/              ← Shiny for Python dashboard
│   ├── app.py
│   ├── db.py
│   ├── charts.py
│   └── requirements.txt
├── frontend/               ← React + TypeScript app
│   ├── src/
│   │   ├── api/            ← Axios API calls
│   │   ├── components/     ← Reusable UI components
│   │   ├── context/        ← Auth & Cart context
│   │   ├── pages/          ← Page components
│   │   └── types/          ← TypeScript type definitions
│   └── vite.config.ts
├── templates/
│   └── admin/
│       └── analytics_dashboard.html
├── seed_orders.py          ← Sample data seeder
├── manage.py
└── README.md
```

---

## Prerequisites

Make sure you have the following installed on your Mac:

- **Python 3.10+** — `python3 --version`
- **Node.js 18+** — `node --version`
- **npm 9+** — `npm --version`
- **pip** — comes with Python

---

## Local Setup

The project has three servers that run simultaneously:

| Server | Port | Description |
|---|---|---|
| Django API | 8000 | Backend + REST API |
| React frontend | 5173 | User-facing store |
| Shiny dashboard | 8001 | Analytics dashboard |

---

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd django_store
```

---

### 2. Django Backend

#### Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Python dependencies

```bash
pip install django
pip install pillow
pip install djangorestframework
pip install django-cors-headers
pip install djangorestframework-simplejwt
pip install pandas
pip install scikit-learn
pip install numpy
pip install sqlalchemy
```

Or install all at once:

```bash
pip install django pillow djangorestframework django-cors-headers djangorestframework-simplejwt pandas scikit-learn numpy sqlalchemy
```

#### Apply migrations

```bash
python3 manage.py migrate
```

#### Create a superuser

```bash
python3 manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

#### Seed sample data (optional but recommended)

This creates 90 days of order history so the ML forecast model has data to work with:

```bash
python3 seed_orders.py
```

> Make sure you have added at least a few Products and Categories via the admin panel before running this.

#### Start the Django server

```bash
python3 manage.py runserver
```

Django is now running at **http://127.0.0.1:8000**

---

### 3. React Frontend

Open a new terminal tab.

#### Install Node dependencies

```bash
cd frontend
npm install
```

This installs:

- `react` + `react-dom`
- `react-router-dom` — client-side routing
- `axios` — HTTP client
- `@tanstack/react-query` — data fetching & caching
- `bootstrap` — CSS framework
- `recharts` — chart components
- `typescript` + `@types/*` — TypeScript support

#### Start the React dev server

```bash
npm run dev
```

React is now running at **http://localhost:5173**

---

### 4. Shiny Analytics Dashboard

Open a third terminal tab.

#### Create and activate a separate virtual environment

```bash
cd analytics
python3 -m venv venv
source venv/bin/activate
```

#### Install Shiny dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install shiny
pip install pandas
pip install sqlalchemy
pip install plotly
pip install python-dotenv
pip install scikit-learn
pip install numpy
```

#### Start the Shiny server

```bash
shiny run app.py --reload --port 8001
```

Shiny dashboard is now running at **http://localhost:8001**

It is also embedded inside Django admin at **http://127.0.0.1:8000/admin/dashboard/**

---

## Running Everything Together

You need three terminal tabs open simultaneously:

```bash
# Terminal 1 — Django backend
cd django_store
source venv/bin/activate
python3 manage.py runserver

# Terminal 2 — React frontend
cd django_store/frontend
npm run dev

# Terminal 3 — Shiny dashboard
cd django_store/analytics
source venv/bin/activate
shiny run app.py --reload --port 8001
```

---

## Available URLs

### Store (React)

| URL | Description |
|---|---|
| `http://localhost:5173/` | Product catalog |
| `http://localhost:5173/products/:slug` | Product detail |
| `http://localhost:5173/cart` | Shopping cart |
| `http://localhost:5173/checkout` | Checkout (login required) |
| `http://localhost:5173/orders` | Order history (login required) |
| `http://localhost:5173/orders/:id` | Order detail (login required) |
| `http://localhost:5173/forecast` | Sales forecast chart (login required) |
| `http://localhost:5173/profile` | User profile (login required) |
| `http://localhost:5173/login` | Login |
| `http://localhost:5173/register` | Register |

### Django Admin

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/admin/` | Django admin panel |
| `http://127.0.0.1:8000/admin/dashboard/` | Shiny analytics dashboard (staff only) |

### REST API

#### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | ❌ | Register new user |
| POST | `/api/auth/login/` | ❌ | Login, returns JWT tokens |
| POST | `/api/auth/token/refresh/` | ❌ | Refresh access token |
| GET/PUT | `/api/auth/profile/` | ✅ | View or update profile |

#### Products
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/products/` | ❌ | List all products |
| GET | `/api/products/?search=query` | ❌ | Search products |
| GET | `/api/products/?category=slug` | ❌ | Filter by category |
| GET | `/api/products/:slug/` | ❌ | Product detail |
| GET | `/api/products/categories/` | ❌ | List all categories |

#### Cart
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/cart/` | ❌ | View cart |
| POST | `/api/cart/add/` | ❌ | Add item to cart |
| DELETE | `/api/cart/remove/:id/` | ❌ | Remove item from cart |
| DELETE | `/api/cart/clear/` | ❌ | Clear entire cart |

#### Orders
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/orders/` | ✅ | List user's orders |
| POST | `/api/orders/create/` | ✅ | Place an order |
| GET | `/api/orders/:id/` | ✅ | Order detail |

#### Forecasting
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/forecast/revenue/?days=30` | ✅ | Revenue forecast |
| GET | `/api/forecast/products/?days=30` | 🔒 Staff only | Product demand forecast |

---

## Features

### Store
- Product catalog with search and category filtering
- Product detail pages with stock indicator
- Session-based shopping cart (works for guests)
- User registration and login with JWT authentication
- Checkout with shipping details form
- Order history and order detail pages
- Persistent cart across pages

### Admin
- Full Django admin panel for managing products, categories, orders, and users
- Order status management with inline order items
- Shiny analytics dashboard embedded in admin sidebar

### Analytics Dashboard (Shiny)
- Total revenue, orders, average order value, and low stock KPIs
- Revenue over time area chart
- Sales by category bar chart
- Order status breakdown donut chart
- Top products table
- Low stock inventory alerts
- Date range filter (7 / 30 / 90 days / all time)
- Adjustable low stock threshold

### Sales Forecasting (ML)
- 7 / 30 / 60 / 90 day revenue forecast
- Per-product demand prediction
- Restock alerts with days until stockout
- Polynomial regression model with time-based features
- Interactive forecast chart in React with Recharts
- Forecast panel in Shiny dashboard

---

## Environment Notes

- `DEBUG = True` is set by default for local development
- SQLite is used as the database — `db.sqlite3` is created automatically after migrations
- Media files (product images) are stored in `/media/`
- JWT access tokens expire after **60 minutes**
- JWT refresh tokens expire after **1 day**
- CORS is configured to allow requests from `localhost:3000` and `localhost:5173`

---

## Adding Products

1. Visit **http://127.0.0.1:8000/admin/**
2. Log in with your superuser credentials
3. Go to **Categories** → Add a category (e.g. "Shoes")
4. Go to **Products** → Add products with name, price, stock, and category
5. Make sure **Available** is checked
6. Visit **http://localhost:5173/** to see your products

---

## Troubleshooting

**`python` not found** — use `python3` instead on Mac.

**`pip` not found** — use `pip3` instead, or make sure your virtual environment is active (`source venv/bin/activate`).

**Cart returns 404** — make sure `cart/` and `users/` routes come before the catch-all products route in `store/urls.py`.

**Forecast returns "not enough data"** — run `python3 seed_orders.py` from the project root to generate 90 days of sample orders.

**Shiny dashboard blank in admin** — make sure the Shiny server is running on port 8001 before visiting the admin dashboard page.

**React can't reach the API** — make sure Django is running on port 8000 and the Vite proxy in `vite.config.ts` is configured correctly.

**`ModuleNotFoundError` in Shiny** — make sure you activated the `analytics/venv` environment, not the main Django one.
