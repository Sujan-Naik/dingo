from django.test import TestCase
from django.urls import reverse

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

    def test_team_details_view_status_code(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail',args=[team.team_name]))
        self.assertEqual(response.status_code, 200)

    def test_team_details_template(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail',args=[team.team_name]))
        self.assertTemplateUsed(response, 'team_detail.html')

    def test_team_details_view(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail',args=[team.team_name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, team.team_name)
        self.assertContains(response, self.team_member1.username)
        self.assertContains(response, self.team_member2.username)

    def test_invite_member_success(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        invited_user = User.objects.create_user(username='@inviteduser', password='Password123')
        self.form_input['action'] = 'invite'
        response = self.client.get(reverse('team_detail', args=[team.team_name]))
        self.assertContains(response,invited_user.username)

    def test_team_task_view(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name="test_team")
        task = Task.objects.create(name="test_task",
                                       description="just a test",
                                       deadline="2023-11-16T15:43:22.039Z",
                                       priority=3,
                                       author=self.user,
                                       team=team,
                                       id=10)
        response = self.client.get(reverse('team_detail', args=[team.team_name]))
        self.assertContains(response, task.name)

    def test_if_no_task_in_team(self):
        self.client.login(username=self.user.username, password='Password123')
        team = Team.objects.get(team_name='test_team')
        response = self.client.get(reverse('team_detail', args=[team.team_name]))
        self.assertContains(response, "No tasks in this team")

