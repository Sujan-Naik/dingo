"""Tests of the task creation view."""
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from tasks.forms import CreateTaskForm
from tasks.models import User, Task, Team
from tasks.tests.helpers import reverse_with_next


class SignUpViewTestCase(TestCase):
    """Tests of the task creation view."""

    """ Pre-populates the table with user"""
    fixtures = \
        [
            'tasks/tests/fixtures/default_user.json',
            'tasks/tests/fixtures/default_team.json'
        ]

    def setUp(self):
        self.url = reverse('create_task')
        self.task_time = timezone.now() + timedelta(days=1)
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(team_name='Default Team')
        self.form_input = \
            {
                'name': 'Test',
                'description': 'This is a test task.',
                'deadline': self.task_time,
                'priority': 3,
                'team': self.team.pk,
                'members': [self.user.pk],
            }

    def test_create_task_url(self):
        self.assertEqual(self.url, '/create_task/')

    def test_get_create_task(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTaskForm))
        self.assertFalse(form.is_bound)

    def test_create_task_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_task_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['name'] = 'x' * 51
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTaskForm))
        self.assertTrue(form.is_bound)

    def test_succesful_task_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        task = Task.objects.get(name='Test')
        self.assertEqual(task.name, 'Test')
        self.assertEqual(task.description, 'This is a test task.')
        self.assertEqual(task.deadline, self.task_time)
        self.assertEqual(task.priority, 3)
        self.assertEqual(task.author, self.user)
