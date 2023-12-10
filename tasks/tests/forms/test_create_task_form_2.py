"""Unit tests of the second page of the create task form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from tasks.forms import CreateTaskForm1, CreateTaskForm2
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
        self.form1_input = \
        {
            'name': 'Coursework',
            'description': 'This is an important django project to finish.',
            'deadline': deadline,
            'priority': 3,
            'team': self.team.pk,
        }

        self.form2_input = \
            {
                'members': [self.user.pk]
            }

    def test_valid_create_task_form(self):
        form = CreateTaskForm2(user=self.user, team=self.team, data=self.form2_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateTaskForm2(user=self.user, team=self.team, data=self.form2_input)
        self.assertIn('members', form.fields)

        members_field = form.fields['members']
        self.assertTrue(isinstance(members_field, forms.ModelMultipleChoiceField))
        checkbox_widget = members_field.widget
        self.assertTrue(isinstance(checkbox_widget, forms.CheckboxSelectMultiple))

    def test_form_must_have_user(self):
        form = CreateTaskForm2(user=None, team=self.team, data=self.form2_input)
        form.full_clean()
        self.assertFalse(form.is_valid())

    def test_form_must_have_team(self):
        form = CreateTaskForm2(user=self.user, team=None, data=self.form2_input)
        form.full_clean()
        self.assertFalse(form.is_valid())
