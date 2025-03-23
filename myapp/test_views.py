from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from myapp.views import user_login  # Adjust based on your actual app structure


from django.test import TestCase, Client
from django.contrib.auth.models import CustomUser
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()  # Dynamically fetch the correct user model

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password123')



        # Creating test users with different role_ids
        self.admin_user = User.objects.create_user(username='admin', password='password123')
        self.admin_user.role_id = 4
        self.admin_user.save()

        self.foreman_user = User.objects.create_user(username='foreman', password='password123')
        self.foreman_user.role_id = 3
        self.foreman_user.save()

        self.worker_user = User.objects.create_user(username='worker', password='password123')
        self.worker_user.role_id = 2
        self.worker_user.save()

        self.reporter_user = User.objects.create_user(username='reporter', password='password123')
        self.reporter_user.role_id = 1
        self.reporter_user.save()

    def test_login_admin_redirects_to_admin_dashboard(self):
        """Test if an admin user is redirected to admin_dashboard."""
        response = self.client.post(reverse('user_login'), {'username': 'admin', 'password': 'password123'})
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_login_foreman_redirects_to_foreman_dashboard(self):
        """Test if a foreman user is redirected to foreman_dashboard."""
        response = self.client.post(reverse('user_login'), {'username': 'foreman', 'password': 'password123'})
        self.assertRedirects(response, reverse('foreman_dashboard'))

    def test_login_worker_redirects_to_worker_dashboard(self):
        """Test if a worker user is redirected to worker_dashboard."""
        response = self.client.post(reverse('user_login'), {'username': 'worker', 'password': 'password123'})
        self.assertRedirects(response, reverse('worker_dashboard'))

    def test_login_reporter_redirects_to_reporter_dashboard(self):
        """Test if a reporter user is redirected to reporter_dashboard."""
        response = self.client.post(reverse('user_login'), {'username': 'reporter', 'password': 'password123'})
        self.assertRedirects(response, reverse('reporter_dashboard'))

    def test_invalid_login_returns_200_and_shows_error(self):
        """Test if invalid login does not redirect but reloads login page with an error."""
        response = self.client.post(reverse('user_login'), {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')

    def test_login_page_loads_correctly(self):
        """Test if login page loads correctly with status 200."""
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
