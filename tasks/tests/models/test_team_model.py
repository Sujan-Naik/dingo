from django.test import TestCase
from tasks.models import User
from tasks.models import Team

class TeamModelTestCase(TestCase):
    fixtures = [
        'tasks/tests/fixtures/other_users.json',
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        """Establishes a default team model to perform tests with"""
        self.user1 = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username='@petrapickles')
        self.user4 = User.objects.get(username='@peterpickles')

        self.team = Team.objects.create(
            team_name='TestTeam',
            team_admin=self.user1
        )
        self.team.team_members.set([self.user1, self.user2, self.user3, self.user4])

    def test_create_team(self):
        """Tests whether teams can be created"""
        team = Team.objects.create(
            team_name='CreateTestTeam',
            team_admin=self.user1
        )
        team.team_members.set([self.user1, self.user2, self.user3, self.user4])

        self.assertEqual(team.team_name, 'CreateTestTeam')
        self.assertEqual(team.team_admin,self.user1)
        self.assertCountEqual(team.team_members.all(), [self.user1, self.user2, self.user3, self.user4])

    def test_unique_team_name(self):
        """Tests team names are unique"""
        with self.assertRaises(Exception):
            another_team = Team.objects.create(team_name='TestTeam')
            another_team.team_members.set([self.user1, self.user2, self.user3, self.user4])

    def test_blank_team_name(self):
        """Ensures team names cannot be blank"""
        with self.assertRaises(Exception):
            Team.objects.create(team_name='', team_members=[self.user1, self.user2, self.user3, self.user4])

    def test_blank_team_members(self):
        """Tests team members cannot be empty"""
        with self.assertRaises(Exception):
            Team.objects.create(team_name='TestTeam', team_members=[])

    def test_admin_is_type_user(self):
        """Ensures that the team admin is a user"""
        self.assertTrue(isinstance(self.team.team_admin, User))
