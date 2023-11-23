from django.test import TestCase
from django.urls import reverse
from tasks.models import Task
from datetime import datetime

class TaskDetailViewTest(TestCase):

    def setUpTestData(self):
        # set the date for test
        Task.objects.create(name="Test Task 1",
                            description = 'test task',
                            deadline = datetime.now(),
                            priority = 3)

    def test_task_details_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task.author]))
        self.assertEqual(response.status_code, 200)

    def test_task_details_template(self):
        response = self.client.get(reverse('task_detail', args=[self.task.author]))
        self.assertTemplateUsed(response, 'tasks/task_detail.html')

    def test_task_details_view_task(self):
        response = self.client.get(reverse('task_detail', args=[self.task.author]))
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Due Date')
        self.assertContains(response, 'Description')
        self.assertContains(response, 'Author')
        self.assertContains(response, 'Time Remaining')

