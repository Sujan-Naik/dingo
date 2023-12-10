"""Tests of the task creation view."""
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from tasks.forms import CreateTaskForm1, CreateTaskForm2
from tasks.models import User, Task, Team
from datetime import datetime
from django.utils import timezone


class CreateTaskViewTestCase(TestCase):
    """Tests of the task creation view."""

    """ Pre-populates the table with user"""
    fixtures = \
        [
            'tasks/tests/fixtures/default_user.json',
            'tasks/tests/fixtures/default_team.json'
        ]

    def setUp(self):

        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(team_name='Default Team')

        self.url = reverse('create_task')
        """Need to be logged in before creating a task.
        self.client.force_login(self.user)
        """

    def test_successful_task_creation(self):

        """Need to be logged in before creating a task."""
        self.client.force_login(self.user)

        before_count = Task.objects.count()

        """
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(team_name='Default Team')
        self.url = reverse('create_task')
        self.client.force_login(self.user)
        """

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        deadline = datetime(2024, 12, 15, 16, 00)
        deadline = deadline.replace(tzinfo=timezone.utc)
        self.form1_input = \
            {
                'create_task_wizard-current_step': 0,
                '0-name': 'Coursework',
                '0-description': 'This is an important django project to finish.',
                '0-deadline': deadline,
                '0-priority': 3,
                '0-team': self.team.pk,
            }

        self.form2_input = \
            {
                'create_task_wizard-current_step': 1,
                '1-members': [self.user.pk],
            }

        response = self.client.post(self.url, self.form1_input)

        self.assertEqual(200, response.status_code)
        # Because django by default returns a 200 on a form validation error,
        # we need another way to check this. If this is a re-rendering of the
        # same form it will be bound, otherwise it will not be.
        self.assertFalse(response.context['form'].is_bound)
        self.assertEqual(
            response.context['wizard']['management_form']['current_step'].value(),
            '1'
        )


        response = self.client.post(self.url, self.form2_input)
        self.assertEqual(302, response.status_code)

        """Ensures that the form redirects to the dashboard"""
        self.assertRedirects(response, reverse('dashboard'), status_code=302, target_status_code=200)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)
        #form = response.context['form']
        #self.assertTrue(form.is_bound)
        task = Task.objects.get(name='Coursework')
        self.assertEqual(task.name, 'Coursework')
        self.assertEqual(task.description, 'This is an important django project to finish.')
        self.assertEqual(task.deadline, deadline)
        self.assertEqual(task.priority, 3)
        self.assertEqual(task.author, self.user)


        #self.assertFalse(response.context['form'].is_bound)

    def test_create_task_url(self):
        self.assertEqual(self.url, '/create_task/')

    def test_get_create_task(self):
        """Need to be logged in before creating a task."""
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        """Confirm that the correct template is used"""
        self.assertTemplateUsed(response, 'create_task_wizard.html')
        form = response.context['form']

        """The form should be on the first page"""
        self.assertTrue(isinstance(form, CreateTaskForm1))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_task_creation(self):
        """Need to be logged in before creating a task."""
        self.client.force_login(self.user)

        #self.client.login(username=self.user.username, password='Password123')
        deadline = datetime(2024, 12, 15, 16, 00)
        deadline = deadline.replace(tzinfo=timezone.utc)
        self.form1_input = \
            {
                'create_task_wizard-current_step': 0,
                '0-name': 'Coursework',
                '0-description': 'This is an important django project to finish.',
                '0-deadline': deadline,
                '0-priority': 3,
                '0-team': self.team.pk,
            }
        #self.form1_input = {'name' : 'x' * 51}
        self.form1_input['0-name'] = 'x' * 51
        before_count = Task.objects.count()
        response = self.client.post(self.url, self.form1_input)
        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task_wizard.html')
        form = response.context['form']
        #self.assertTrue(isinstance(form, CreateTaskForm))
        self.assertTrue(form.is_bound)
