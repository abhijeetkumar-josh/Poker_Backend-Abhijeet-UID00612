from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("user:register")
        self.login_url = reverse("user:login")

        self.test_user = User.objects.create_user(
            username='testname',
            email="test@example.com",
            password="strong_password_123"
        )

    def test_register_success(self):
        data = {
            "username":"someusername",
            "email": "newuser@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_email(self):
        data = {
            "username":"testname",
            "email": "test@example.com",
            "password": "Password123!"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        data = {
            "username":"someusername",
            "email": "test@example.com",
            "password": "strong_password_123"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        data = {
            "username":"someusername",
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")
