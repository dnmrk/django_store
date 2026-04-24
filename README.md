# Django Store

A simple e-commerce storefront built with Django 4.2.

## Setup

**Prerequisites:** Python 3.x

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install django pillow

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

- `store/` — Django project settings and root URL config
- `products/` — Product catalog app (models, views, templates)
