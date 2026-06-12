from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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

    def test_add_to_cart_with_existing_session_cookie_does_not_require_csrf_token(self):
        """The SPA cart is session-backed, but it does not read Django's CSRF cookie.

        If a visitor also has a Django session cookie, for example after using
        /admin/, DRF's SessionAuthentication would otherwise reject unsafe cart
        requests with 403 before CartAddView runs.
        """
        User.objects.create_user(username='staff', password='testpass123')
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username='staff', password='testpass123'))

        response = client.post(
            '/api/cart/add/',
            {'product_id': self.product.id, 'quantity': 1},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 1)

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
