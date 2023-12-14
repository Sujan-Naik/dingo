"Test of the Modify Task View"
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from tasks.models import User, Task, Team



class ModifyTaskTestCase(TestCase):


    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='user@gmail.com')
        self.another_user = User.objects.create_user(username='anotheruser', password='testpassword', email='user2@gmail.com')

        # Create a team
        self.team = Team.objects.create(
            team_name='Test Team',
            team_admin=self.user,
        )

        # Add the user to the team
        self.team.invite_member(self.user)
        self.team.invite_member(self.another_user)

        # Create a task associated with the team
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            deadline='2023-12-31',
            priority= 2,
            author=self.user,
            team=self.team,
        )

        self.task.members.set([self.another_user])
    
    def test_modify_task_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Get the URL for the modify task view, replace 'modify-task' with your actual URL pattern name
        url = reverse('modify_task', kwargs={'pk': self.task.id})

        form_data = {
            'name': 'Modified Task',
            'description': 'This task has been modified.',
            'deadline': '2023-12-31',
            'priority': 5,
            'team': self.team.pk,
            'add_members': [self.user.id],  # Add a member not already in the task
            'remove_members': [self.another_user.id],  # Remove a member already in the task
        }

        # Make a POST request to modify the task with the form data
        response = self.client.post(url, data=form_data)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Optionally, you can check that the task has been modified in the database
        modified_task = Task.objects.get(id=self.task.id)
        self.assertEqual(modified_task.name, 'Modified Task')

        # Add assertions for the modified task members based on the form_data
        self.assertIn(self.user, modified_task.members.all())

        # Assertion for the removed member
        self.assertNotIn(self.another_user, modified_task.members.all())








        