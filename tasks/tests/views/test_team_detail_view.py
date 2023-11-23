from django.test import TestCase
from django.urls import reverse

from tasks.forms import CreateTaskForm
from tasks.models import Task, User, Team


class TeamDetailViewTest(TestCase):

    fixtures = ['tasks/tests/fixtures/other_users.json',
                'tasks/tests/fixtures/default_user.json']

    def setUp(self):
        # set the date for test
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

    def test_task_details_view(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail',args=[team.team_name]))
        self.assertEqual(response.status_code, 200)

    def test_task_details_template(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail',args=[team.team_name]))
        self.assertTemplateUsed(response, 'team_detail.html')

    def test_task_details_view_task(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail',args=[team.team_name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, team.team_name)
        self.assertContains(response, self.team_member1.username)
        self.assertContains(response, self.team_member2.username)
