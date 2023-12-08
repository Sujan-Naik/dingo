"""Tests of the task list view."""

from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, User, Team
from tasks.forms import TaskSortForm
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

        new_task = Task.objects.create(name=self.form_input['name'],
                                       description=self.form_input['description'],
                                       deadline=self.form_input['deadline'],
                                       priority=self.form_input['priority'],
                                       author=self.form_input['author'],
                                       team=self.form_input['team'],
                                       id=10)

        new_task.members.set(self.form_input['members'])

    def test_task_list_view(self):
        """Test if the task list exists"""
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)

    def test_template_and_form(self):
        """Test if the template and form are correct"""
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        self.assertTemplateUsed(response,'task_list.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TaskSortForm))
        self.assertFalse(form.is_bound)

    def test_task_list_show_task(self):
        """Test if the list can show the correct task"""
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        task = Task.objects.get(id=10)
        self.assertContains(response, task.name)

    def test_valid_sort(self):
        """Test if the page is correctly returned with a valid sort condition"""
        self.client.login(username=self.user.username, password='Password123')
        sort_conditions = "?sort_by=deadline&asc_or_desc=on&filter_by=name&filter_string=testing"
        response = self.client.get(reverse('task_list') + sort_conditions)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'task_list.html')
        num_tasks = len(response.context['task_list'])
        self.assertEqual(num_tasks,1)

    def test_invalid_sort(self):
        """Test if the page is correctly returned with an invalid sort condition"""
        self.client.login(username=self.user.username, password='Password123')
        sort_conditions = "?sort_by=bob%asc_or_desc=on&filter_by=bad_filter"
        response = self.client.get(reverse('task_list') + sort_conditions)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'task_list.html')
        num_tasks = len(response.context['task_list'])
        self.assertEqual(num_tasks,2)

    def test_task_number(self):
        """Test that the correct number of tasks is displayed with no sort criteria"""
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('task_list'))
        num_tasks = len(response.context['task_list'])
        self.assertEqual(num_tasks,2)

    # test if no task to show
    # def test_no_task(self):
    #     pass
