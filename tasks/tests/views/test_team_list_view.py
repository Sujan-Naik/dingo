"""Tests of the team list view."""

from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, User, Team
from datetime import datetime

class TeamListTestCase(TestCase):
    """Tests of the team list view."""
    fixtures = ['tasks/tests/fixtures/other_users.json',
                'tasks/tests/fixtures/default_user.json']

    def setUp(self):
        # set the data for test
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'team_name': 'test_team',
            'team_admin': self.user,
        }

        self.team = Team.objects.create(team_name=self.form_input['team_name'],
                                        team_admin=self.user)

        self.team_member1 = User.objects.get(username='@johndoe')
        self.team_member2 = User.objects.get(username='@janedoe')
        self.team.team_members.add(self.team_member1, self.team_member2)



    # test if the team list exists
    def test_task_list_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('team_list'))
        self.assertEqual(response.status_code,200)

    # test if the template is correct
    def test_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('team_list'))
        self.assertTemplateUsed(response,'team_list.html')

    # test if the list can show the correct team
    def test_task_list_show_task(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('team_list'))
        self.assertContains(response, self.team.team_name)
