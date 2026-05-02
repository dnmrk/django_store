# Project Overview

## Project Name
Django Store

## Description
A full-stack e-commerce application with a Django REST API backend and React SPA frontend. Supports product browsing, cart management, JWT-authenticated checkout, and order history.

## Tech Stack
- **Backend Framework**: Django 4.2.30
- **API Layer**: Django REST Framework 3.16.1
- **Auth**: djangorestframework-simplejwt 5.5.1
- **Language**: Python 3.9.6
- **Frontend**: React 19 + Vite 8 + React Router 7 + TanStack Query 5
- **Styling**: Bootstrap 5.3
- **HTTP Client**: Axios
- **Database**: SQLite (development)
- **Media**: Pillow 11.3 (image uploads)

## Project Type
Full-stack web application (Django API + React SPA)

## Django Apps
- `products` — Product catalog: Category and Product models, storefront views, REST API
- `cart` — Session-based cart management with REST API
- `orders` — Order model, checkout flow, order history API
- `users` — User registration/login, JWT auth endpoints
- `store` — Project config (settings, root URLs, wsgi/asgi)

## Frontend (frontend/)
React SPA that consumes the Django REST API. Auth state managed via JWT tokens stored in localStorage. Cart state managed via React Context. Data fetching via TanStack Query + Axios.
