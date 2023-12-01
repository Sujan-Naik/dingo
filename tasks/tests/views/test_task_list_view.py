"""Tests of the task list view."""

from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, User, Team
from datetime import datetime

class TaskListTestCase(TestCase):
    """Tests of the task list view."""

    """ Pre-populates the table with user"""
    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/default_team.json',
        'tasks/tests/fixtures/default_task.json',
    ]

    def setUp(self):
        # set the date for test
        self.user = User.objects.get(username='@johndoe')
        self.team = Team.objects.get(team_name='Default Team')
        self.form_input = {
            'name': 'Test',
            'description': 'This is a test task.',
            'deadline': "2023-11-16T15:43:22.039Z",
            'priority': 3,
            'author': self.user,
            'team': self.team,
            'members': [self.user.pk]
        }

        new_task = Task.objects.create(name = self.form_input['name'],
                            description = self.form_input['description'],
                            deadline = self.form_input['deadline'],
                            priority = self.form_input['priority'],
                            author = self.form_input['author'],
                            team=self.form_input['team'])

        new_task.members.set(self.form_input['members'])

    # test if the task list exists
    def test_task_list_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code,200)

    # test if the template is correct
    def test_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        self.assertTemplateUsed(response,'task_list.html')

    # test if the list can show the correct task
    def test_task_list_show_task(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        task = Task.objects.get(name='Test')
        self.assertContains(response, task.name)

    # test if no task to show
    # def test_no_task(self):
    #     pass

    # test if has many tasks to show, the number of tasks
    # def test_task_number(self):
    #     pass


