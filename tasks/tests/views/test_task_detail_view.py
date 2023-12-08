from django.utils import timezone

from django.test import TestCase
from django.urls import reverse

from tasks.forms import CreateTaskForm
from tasks.models import Task, User, Team, TimeLogging


class TaskDetailViewTest(TestCase):
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
        self.task = Task.objects.get(name='Testing')

        new_task = Task.objects.create(name=self.form_input['name'],
                                       description=self.form_input['description'],
                                       deadline=self.form_input['deadline'],
                                       priority=self.form_input['priority'],
                                       author=self.form_input['author'],
                                       team=self.form_input['team'],
                                       id=10)

        new_task.members.set(self.form_input['members'])

    def test_task_details_view(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        response = self.client.get(reverse('task_detail',args=[task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_details_template(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        response = self.client.get(reverse('task_detail',args=[task.id]))
        self.assertTemplateUsed(response, 'task_detail.html')

    def test_task_details_view_task(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        response = self.client.get(reverse('task_detail',args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.name)
        self.assertContains(response, task.description)
        self.assertContains(response, task.author)
        self.assertContains(response, task.priority)

    def test_task_details_view_timeLogging(self):
        self.client.login(username=self.user.username, password='Password123')
        task = Task.objects.get(name='Test')
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=2)

        # Create a valid TimeLogging entry
        time_logging = TimeLogging.objects.create(
            user=self.user,
            task=task,
            start_time=start_time,
            end_time=end_time,
        )
        time_logging.user = self.user
        time_logging.task = task
        time_logging.start_time = start_time
        time_logging.end_time = end_time
        response = self.client.get(reverse('task_detail', args=[task.id]))

        expected_output = f"{self.user.username} spent"

        self.assertContains(response,self.user.username)
        self.assertContains(response, task.name)
        print(response.content.decode())
        self.assertContains(response, expected_output)

