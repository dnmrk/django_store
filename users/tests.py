from unittest.mock import patch

from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.throttling import ScopedRateThrottle


class LogoutAPITests(APITestCase):
    def setUp(self):
        cache.clear()  # throttle counters persist across tests otherwise

    def register(self):
        return self.client.post(
            '/api/auth/register/',
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'a-strong-pass-123',
                'password2': 'a-strong-pass-123',
            },
            format='json',
        )

    def test_logout_blacklists_refresh_token(self):
        tokens = self.register().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        response = self.client.post(
            '/api/auth/logout/', {'refresh': tokens['refresh']}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # The blacklisted refresh token can no longer mint access tokens.
        refresh_response = self.client.post(
            '/api/auth/token/refresh/', {'refresh': tokens['refresh']}, format='json'
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_requires_authentication(self):
        response = self.client.post('/api/auth/logout/', {'refresh': 'x'}, format='json')
        # SessionAuthentication is the first authenticator, so DRF answers 403
        # (no WWW-Authenticate challenge) rather than 401.
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_logout_without_refresh_token_fails(self):
        tokens = self.register().data
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.post('/api/auth/logout/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthThrottleTests(APITestCase):
    def setUp(self):
        cache.clear()

    # THROTTLE_RATES is a class attribute snapshotted from settings at import
    # time, so override_settings(REST_FRAMEWORK=...) cannot change it.
    @patch.object(ScopedRateThrottle, 'THROTTLE_RATES', {'auth': '3/min'})
    def test_login_is_throttled(self):
        for _ in range(3):
            response = self.client.post(
                '/api/auth/login/',
                {'username': 'ghost', 'password': 'wrong'},
                format='json',
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(
            '/api/auth/login/',
            {'username': 'ghost', 'password': 'wrong'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
