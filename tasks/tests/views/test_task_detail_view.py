from django.test import TestCase
from django.urls import reverse

from tasks.forms import CreateTaskForm
from tasks.models import Task, User


class TaskDetailViewTest(TestCase):

    fixtures = ['tasks/tests/fixtures/default_task.json',
                'tasks/tests/fixtures/default_user.json']

    def setUp(self):
        # set the date for test
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'name': 'Test',
            'description': 'This is a test task.',
            'deadline': "2023-11-16T15:43:22.039Z",
            'priority': 3,
            'author': self.user
        }

        Task.objects.create(name = self.form_input['name'],
                            description = self.form_input['description'],
                            deadline = self.form_input['deadline'],
                            priority = self.form_input['priority'],
                            author = self.form_input['author'])

    def test_task_details_view(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        response = self.client.get(reverse('task_detail',args=[task.name]))
        self.assertEqual(response.status_code, 200)

    def test_task_details_template(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        response = self.client.get(reverse('task_detail',args=[task.name]))
        self.assertTemplateUsed(response, 'task_detail.html')

    def test_task_details_view_task(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        response = self.client.get(reverse('task_detail',args=[task.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.name)
        self.assertContains(response, task.description)
        self.assertContains(response, task.author)
        self.assertContains(response, task.priority)

