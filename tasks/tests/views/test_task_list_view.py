"""Tests of the task list view."""

from django.test import TestCase
from django.urls import reverse

from tasks.models import Task
from datetime import datetime

class TaskListTestCase(TestCase):
    """Tests of the task list view."""

    def setUpTestData(self):
        # set the date for test
        Task.objects.create(name="Test Task 1",
                            description = 'test task',
                            deadline = datetime.now(),
                            priority = 3)

    # test if the task list exists
    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code,200)

    # test if the template is correct
    def test_template(self):
        response = self.client.get(reverse('task_list'))
        self.assertTemplateUsed(response,'tasks/task_list.html')

    # test if the list can show the correct task
    def test_task_list_show_task(self):
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Test Task 1')

    # test if no task to show
    def test_no_task(self):
        pass

    # test if has many tasks to show, the number of tasks
    def test_task_number(self):
        pass


