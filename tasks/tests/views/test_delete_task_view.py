from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task, Team

class TaskTests(TestCase):
    def setUp(self):
        # Create a user for authentication
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
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Get the URL for the delete task view, replace 'delete-task' with your actual URL pattern name
        url = reverse('delete_task', kwargs={'pk': self.task.id})

        # Make a GET request to the delete task view
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Optionally, you can check for specific content in the response, if needed

        # Make a POST request to confirm the deletion
        response = self.client.post(url)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the task was deleted
        self.assertFalse(Task.objects.filter(pk=self.task.id).exists())