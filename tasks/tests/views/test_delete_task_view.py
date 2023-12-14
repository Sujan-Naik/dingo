from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task, Team

class TaskTests(TestCase):
    def setUp(self):
        """set the default data"""
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a team
        self.team = Team.objects.create(
            team_name='Test Team',
            team_admin=self.user,
        )

        # Add the user to the team
        self.team.invite_member(self.user)

        # Create a task associated with the team
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            deadline='2023-12-31',
            priority= 3,
            author=self.user,
            team=self.team,
        )

    def test_delete_task_view(self):
        """test the view if the task is deleted"""
        self.client.login(username='testuser', password='testpassword')
        url = reverse('delete_task', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.id).exists())