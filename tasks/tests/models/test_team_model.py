from django.test import TestCase
from tasks.models import User
from tasks.models import Team

class TeamModelTestCase(TestCase):
    fixtures = [
        'tasks/tests/fixtures/other_users.json',
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username='@petrapickles')
        self.user4 = User.objects.get(username='@peterpickles')

    def test_create_team(self):
        team = Team.objects.create(
            team_name='TestTeam'
        )
        team.team_members.set([self.user1, self.user2, self.user3, self.user4])

        self.assertEqual(team.team_name, 'TestTeam')
        self.assertCountEqual(team.team_members.all(), [self.user1, self.user2, self.user3, self.user4])

    def test_unique_team_name(self):
        team = Team.objects.create(team_name='TestTeam')
        team.team_members.set([self.user1, self.user2, self.user3, self.user4])

        with self.assertRaises(Exception):
            another_team = Team.objects.create(team_name='TestTeam')
            another_team.team_members.set([self.user1, self.user2, self.user3, self.user4])

    def test_blank_team_name(self):
        with self.assertRaises(Exception):
            Team.objects.create(team_name='', team_members=[self.user1, self.user2, self.user3, self.user4])

    def test_blank_team_members(self):
        with self.assertRaises(Exception):
            Team.objects.create(team_name='TestTeam', team_members=[])

