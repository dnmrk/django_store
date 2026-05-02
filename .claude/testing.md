# Testing Configuration

## Test Framework
Django built-in test runner (unittest-based, `python manage.py test`)

## TDD Methodology

Each task follows strict Red → Green → Refactor:

1. Write failing test for one requirement
2. Write minimum code to pass
3. Refactor while tests stay green
4. Repeat for next requirement
5. Commit when task complete

## Commands

```bash
# Activate venv first
source venv/bin/activate

# Run all tests (parallel — default)
python manage.py test --parallel

# Run all tests (sequential — use when debugging flaky parallel failures)
python manage.py test

# Run a specific app
python manage.py test products

# Run a specific test case
python manage.py test products.tests.ProductListAPITest

# Run a specific test method
python manage.py test products.tests.ProductListAPITest.test_returns_available_products

# Run with verbosity
python manage.py test --verbosity=2
```

## Parallel Execution
- **Default**: Always run tests in parallel unless debugging a specific failure
- Parallel command: `python manage.py test --parallel`
- Sequential fallback: `python manage.py test`

## Test File Locations
- Each app has its own `tests.py` (or `tests/` package for larger suites):
  - `products/tests.py`
  - `cart/tests.py`
  - `orders/tests.py`
  - `users/tests.py`

## Coverage Requirements
- Minimum: 80%
- New code must have tests

## Test Naming Convention
- Test classes: `{Feature}Test` (e.g., `ProductListAPITest`, `CartAddItemTest`)
- Test methods: `test_{what_it_does}` (e.g., `test_returns_404_for_unknown_product`)

## API Test Pattern
Use `rest_framework.test.APITestCase` for API endpoint tests:
```python
from rest_framework.test import APITestCase
from rest_framework import status

class ProductListAPITest(APITestCase):
    def test_returns_available_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

## Auth Test Pattern
For JWT-protected endpoints, obtain a token first:
```python
def setUp(self):
    self.user = User.objects.create_user(username='test', password='pass')
    response = self.client.post('/api/auth/token/', {'username': 'test', 'password': 'pass'})
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
```
