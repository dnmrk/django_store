from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product
from .models import Order, OrderItem


SHIPPING_DATA = {
    'full_name': 'Test Buyer',
    'email': 'buyer@example.com',
    'address': '1 Test Street',
    'city': 'Testville',
    'postal_code': '12345',
}


class OrderCreateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='test-pass-123')
        category = Category.objects.create(name='Widgets', slug='widgets')
        self.product = Product.objects.create(
            category=category,
            name='Widget',
            slug='widget',
            price=Decimal('10.00'),
            stock=10,
        )

    def add_to_cart(self, quantity=2):
        return self.client.post(
            '/api/cart/add/',
            {'product_id': self.product.id, 'quantity': quantity},
            format='json',
        )

    def test_create_order_requires_authentication(self):
        response = self.client.post('/api/orders/create/', SHIPPING_DATA, format='json')
        # SessionAuthentication is the first authenticator, so DRF answers 403
        # (no WWW-Authenticate challenge) rather than 401.
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_create_order_with_empty_cart_fails(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/orders/create/', SHIPPING_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_items_use_current_product_price_not_cart_price(self):
        self.client.force_authenticate(user=self.user)
        self.add_to_cart(quantity=2)

        # Price changes after the item was added to the cart.
        self.product.price = Decimal('15.00')
        self.product.save()

        response = self.client.post('/api/orders/create/', SHIPPING_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        item = OrderItem.objects.get(order__user=self.user)
        self.assertEqual(item.price, Decimal('15.00'))
        self.assertEqual(item.quantity, 2)

    def test_create_order_clears_cart(self):
        self.client.force_authenticate(user=self.user)
        self.add_to_cart()
        self.client.post('/api/orders/create/', SHIPPING_DATA, format='json')

        response = self.client.get('/api/cart/')
        self.assertEqual(response.data['total_items'], 0)

    def test_invalid_shipping_data_creates_no_order(self):
        self.client.force_authenticate(user=self.user)
        self.add_to_cart()
        response = self.client.post(
            '/api/orders/create/', {**SHIPPING_DATA, 'email': 'not-an-email'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)


class OrderOwnershipAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='test-pass-123')
        self.other = User.objects.create_user(username='other', password='test-pass-123')
        self.order = Order.objects.create(user=self.owner, **SHIPPING_DATA)

    def test_users_only_see_their_own_orders(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_fetch_another_users_order(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
