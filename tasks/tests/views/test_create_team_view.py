from django.test import TestCase, Client
from tasks.models import User
from django.urls import reverse
from tasks.models import Team
from tasks.forms import TeamCreateForm
from django.contrib.messages import get_messages

class TeamViewTest(TestCase):


    fixtures = [
        'tasks/tests/fixtures/other_users.json',
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_team_view_get(self):
        response = self.client.get(reverse('team'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team.html')
        self.assertIsInstance(response.context['form'], TeamCreateForm)


    def test_team_view_post_valid_form(self):
        self.form_input = {
            'team_name': 'TestTeam',
            'team_members': [User.objects.get(username='@johndoe'),
                             User.objects.get(username='@janedoe'),
                             User.objects.get(username='@petrapickles'),
                             User.objects.get(username='@peterpickles')]
        }

        response = self.client.post(reverse('team'), data=self.form_input)
        """200 is successful, 302 is a redirect"""
        self.assertTrue(response.status_code in [200, 302])
        if response.status_code == 302:
            self.assertRedirects(response, reverse('dashboard'))

        self.assertEqual(Team.objects.count(), 1)
        team = Team.objects.get(team_name='TestTeam')
        self.assertEqual(team.team_name, 'TestTeam')
        TeamMembers = sorted(list(team.team_members.all()), key=lambda user: user.username)
        expected_users = [
            User.objects.get(username='@johndoe'),
            User.objects.get(username='@janedoe'),
            User.objects.get(username='@petrapickles'),
            User.objects.get(username='@peterpickles')
        ]
        expected_users = sorted(expected_users, key=lambda user: user.username)
        self.assertEqual(TeamMembers, expected_users)

        # Check if success message is present
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Team created!", messages)



    def test_team_view_post_invalid_form(self):
        # Create a team with the same name to make the form invalid
        Team.objects.create(team_name='TestTeam').team_members.set([self.user.id])

        team_data = {
            'team_name': 'TestTeam',
            'team_members': [self.user.id],
        }
        response = self.client.post(reverse('team'), data=team_data)
        self.assertEqual(response.status_code, 200)  # Expecting the form to be rendered again
        self.assertTemplateUsed(response, 'team.html')
        self.assertIsInstance(response.context['form'], TeamCreateForm)

        # Check if error message is present
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Form submission failed. Please check the form for errors.", messages)
