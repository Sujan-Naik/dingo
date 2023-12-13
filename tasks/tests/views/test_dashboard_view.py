"""Tests of the dashboard view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User
from tasks.forms import TimezoneForm

class DashboardViewTestCase(TestCase):
    """Tests of the dashboard view."""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='@johndoe')

    def test_dashboard_url(self):
        """Test that url is correct"""
        self.assertEqual(self.url,'/dashboard/')

    def test_get_dashboard(self):
        """Test that dashboard is correctly displayed when user is logged-in"""
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        form = response.context['timezone_form']
        self.assertTrue(isinstance(form, TimezoneForm))

    def test_timezone_displayed_in_form(self):
        """Test that user's timezone is correctly displayed in the timezone form"""
        self.client.login(username=self.user.username, password="Password123")
        session = self.client.session
        session['django_timezone'] = 'Europe/London'
        session.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        form = response.context['timezone_form']
        self.assertTrue(isinstance(form, TimezoneForm))
        self.assertEqual(form.data['timezone'], 'Europe/London')

    def test_get_dashboard_redirects_when_not_logged_in(self):
        """Test user is redirected to the login page if not logged in"""
        response = self.client.get(self.url, follow=True)
        redirect_url = '/log_in/?next=/dashboard/'
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')
