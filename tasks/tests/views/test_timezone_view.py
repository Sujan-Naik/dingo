"""Tests of the timezone view"""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User

class TimezoneViewTestCase(TestCase):
    """Tests of the timezone view"""

    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('timezone')
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {'timezone' : 'Europe/London'}

    def test_get_redirects_when_logged_in(self):
        """Test that a logged-in user is redirected if they send a GET request"""
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('timezone')
        response = self.client.get(self.url)
        redirect_url = '/'
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=302)

    def test_get_redirects_when_logged_out(self):
        """Test that a user that isn't logged-in is redirected if they send a GET request"""
        self.url = reverse('timezone')
        response = self.client.get(self.url)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_valid_timezone_selection(self):
        """Test that timezone is correctly applied"""
        self.client.login(username=self.user.username, password="Password123")
        header = {'HTTP_REFERER' : reverse('dashboard')}
        response = self.client.post(self.url, self.form_input, **header)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        session = self.client.session
        self.assertEqual(session['django_timezone'], 'Europe/London')
