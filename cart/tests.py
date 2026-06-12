from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product


class CartAPITests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name='Widgets', slug='widgets')
        self.product = Product.objects.create(
            category=category,
            name='Widget',
            slug='widget',
            price=Decimal('19.99'),
            stock=10,
        )

    def add(self, quantity):
        return self.client.post(
            '/api/cart/add/',
            {'product_id': self.product.id, 'quantity': quantity},
            format='json',
        )

    def test_add_to_cart(self):
        response = self.add(quantity=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 3)

    def test_quantity_above_maximum_is_rejected(self):
        response = self.add(quantity=100)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_quantity_below_minimum_is_rejected(self):
        response = self.add(quantity=0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_price_is_exact_decimal(self):
        self.add(quantity=3)
        response = self.client.get('/api/cart/')
        # 3 * 19.99 must be exactly 59.97 — float math would drift.
        self.assertEqual(Decimal(str(response.data['total_price'])), Decimal('59.97'))
