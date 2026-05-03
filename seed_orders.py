"""
Seed script: generates 60 days of realistic order history for the revenue forecast chart.

Usage:
    source venv/bin/activate
    python seed_orders.py
"""
import os
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")

import django
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Category, Product
from orders.models import Order, OrderItem

SEED = 42
random.seed(SEED)

# ── Catalogue ─────────────────────────────────────────────────────────────────

CATALOGUE = [
    ("Apparel",     [("T-Shirt", "t-shirt", 599.00, 150),
                     ("Polo Shirt", "polo-shirt", 899.00, 80),
                     ("Hoodie", "hoodie", 1499.00, 60)]),
    ("Footwear",    [("Sneakers", "sneakers", 2499.00, 40),
                     ("Sandals", "sandals", 799.00, 90)]),
    ("Accessories", [("Cap", "cap", 399.00, 200),
                     ("Belt", "belt", 499.00, 70),
                     ("Watch", "watch", 3999.00, 30)]),
    ("Electronics", [("Earbuds", "earbuds", 1299.00, 50),
                     ("Phone Case", "phone-case", 299.00, 120)]),
]

STATUSES = ["pending", "processing", "shipped", "delivered"]
STATUS_WEIGHTS = [0.10, 0.15, 0.30, 0.45]


def get_or_create_user():
    user, _ = User.objects.get_or_create(
        username="seed_customer",
        defaults={"email": "seed@example.com", "first_name": "Seed", "last_name": "Customer"},
    )
    if not user.has_usable_password():
        user.set_password("testpass123")
        user.save()
    return user


def populate_catalogue():
    products = []
    for cat_name, items in CATALOGUE:
        cat, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={"slug": cat_name.lower()},
        )
        for name, slug, price, stock in items:
            p, _ = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": cat,
                    "name": name,
                    "price": Decimal(str(price)),
                    "stock": stock,
                    "available": True,
                },
            )
            products.append(p)
    return products


def daily_order_count(date: datetime) -> int:
    """More orders on weekends; slight mid-month bump."""
    base = 4
    if date.weekday() >= 5:
        base += 3
    if 12 <= date.day <= 18:
        base += 2
    return base + random.randint(-1, 2)


def seed_orders(days: int = 60):
    user = get_or_create_user()
    products = populate_catalogue()

    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = today - timedelta(days=days)

    created = 0
    for day_offset in range(days):
        day = start + timedelta(days=day_offset)
        count = daily_order_count(day)

        for _ in range(count):
            order_time = day + timedelta(
                hours=random.randint(8, 22),
                minutes=random.randint(0, 59),
            )
            status = random.choices(STATUSES, STATUS_WEIGHTS)[0]

            order = Order(
                user=user,
                full_name="Seed Customer",
                email="seed@example.com",
                address="123 Seed Street",
                city="Manila",
                postal_code="1000",
                status=status,
            )
            order.save()
            # Override auto_now_add timestamp
            Order.objects.filter(pk=order.pk).update(created_at=order_time)

            items_count = random.randint(1, 3)
            chosen = random.sample(products, min(items_count, len(products)))
            for product in chosen:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 4),
                    price=product.price,
                )
            created += 1

    print(f"Created {created} orders across {days} days.")
    print("Revenue forecast chart should now have enough data.")


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed_orders(days)
