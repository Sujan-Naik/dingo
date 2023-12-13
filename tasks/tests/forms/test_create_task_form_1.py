"""Unit tests of the first page of the create task form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from tasks.forms import CreateTaskForm1
from tasks.models import Task, User, Team
from datetime import datetime
from django.utils import timezone


class CreateTaskFormTestCase(TestCase):
    """Unit tests of the first page of the create task form."""

    """ Pre-populates the table with default user and default team"""
    fixtures = \
        [
            'tasks/tests/fixtures/default_user.json',
            'tasks/tests/fixtures/default_team.json'
        ]

    def setUp(self):
        deadline = datetime(2024, 12, 15, 16, 00)
        deadline = deadline.replace(tzinfo=timezone.utc)
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(team_name='Default Team')
        self.form_input = \
        {
            'name': 'Coursework',
            'description': 'This is an important django project to finish.',
            'deadline': deadline,
            'priority': 3,
            'team': self.team.pk,
        }

    def test_valid_create_task_form(self):
        form = CreateTaskForm1(user=self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateTaskForm1()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('deadline', form.fields)
        self.assertIn('priority', form.fields)
        self.assertIn('team', form.fields)

        deadline_field = form.fields['deadline']
        self.assertTrue(isinstance(deadline_field, forms.DateTimeField))
        datetime_widget = form.fields['deadline'].widget
        self.assertTrue(isinstance(datetime_widget, forms.DateTimeInput))

    def test_deadline_must_be_in_future(self):
        past_datetime = datetime(2020, 12, 15, 16, 00)
        past_datetime = past_datetime.replace(tzinfo=timezone.utc)
        self.form_input['deadline'] = past_datetime
        form = CreateTaskForm1(user=self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_have_user(self):
        form = CreateTaskForm1(user=None, data=self.form_input)
        form.full_clean()
        self.assertFalse(form.is_valid())
