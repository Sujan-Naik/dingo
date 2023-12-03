"""Unit tests of the create task form wizard with both pages."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from tasks.forms import CreateTaskForm1, CreateTaskForm2
from tasks.models import Task, User, Team
from datetime import datetime
from django.utils import timezone


class CreateTaskFormTestCase(TestCase):
    """Unit tests of the create task form wizard with both pages."""

    """ Pre-populates the table with user"""
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

    def test_valid_create_task_forms(self):
        form1 = CreateTaskForm1(user=self.user, data=self.form1_input)
        self.assertTrue(form1.is_valid())
        form2 = CreateTaskForm2(user=self.user, team=self.team, data=self.form2_input)
        self.assertTrue(form2.is_valid())

    def test_form_wizard_must_save_correctly(self):
        form1 = CreateTaskForm1(user=self.user, data=self.form1_input)
        form2 = CreateTaskForm2(user=self.user, team=self.team, data=self.form2_input)
        before_count = Task.objects.count()
        form2.save()
        after_count = Task.objects.count()
        #self.assertEqual(after_count, before_count + 1)
        task = Task.objects.get(name='Coursework')

        self.assertEqual(task.name, 'Coursework')
        self.assertEqual(task.description, 'This is an important django project to finish.')
        deadline = timezone.datetime(2024, 12, 15, 16, 00)
        deadline = deadline.replace(tzinfo=timezone.utc)
        self.assertEqual(task.deadline, deadline)
