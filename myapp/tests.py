from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from myapp.views import user_login  # Adjust based on your actual app structure


class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('user_login')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful login
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on the login page
        self.assertContains(response, "Invalid username or password")

    def test_login_with_empty_username(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on the login page
        self.assertContains(response, "This field is required.")

    def test_login_with_empty_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)  # Stays on the login page
        self.assertContains(response, "This field is required.")

    def test_login_with_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on the login page
        self.assertContains(response, "Invalid username or password")

    def test_login_with_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stays on the login page
        self.assertContains(response, "This account is inactive.")

    def test_login_get_request(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)  # Renders the login page
        self.assertTemplateUsed(response, 'login.html')