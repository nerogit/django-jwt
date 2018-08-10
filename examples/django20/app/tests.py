from django_jwt import create_access_token

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import (
    TestCase,
)


class ViewTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.username = 'test'
        self.password = 'passwd'
        self.user = user_model.objects.create_user(
            username=self.username,
            email='test@example.com',
            password=self.password
        )
        self.access_token = create_access_token(self.user)

    def test_sign_in(self):
        data = {
            "username": self.username,
            "password": self.password,
        }
        resp = self.client.post('/sign-in/', data=data, headers={''})
        recv_data = resp.json()
        self.assertEqual(200, resp.status_code)
        self.assertEqual(['accessToken'], list(recv_data.keys()))

    def test_fbv(self):
        headers = {
            "HTTP_Authorization": f'Bearer {self.access_token}',
        }
        resp = self.client.get('/fbv', **headers)
        self.assertEqual(200, resp.status_code)
        recv_data = resp.json()
        self.assertEqual({"username": self.username}, recv_data)

    def test_cbv(self):
        headers = {
            "HTTP_Authorization": f'Bearer {self.access_token}',
        }
        resp = self.client.get('/cbv', **headers)
        self.assertEqual(200, resp.status_code)
        recv_data = resp.json()
        self.assertEqual({"username": self.username}, recv_data)

    def test_unauthorized_access(self):
        resp = self.client.get('/fbv')
        self.assertEqual(401, resp.status_code)
        self.assertIn(settings.ERROR_MESSAGE_KEY, resp.json().keys())
