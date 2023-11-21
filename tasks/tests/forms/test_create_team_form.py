"""Unit tests of the create team form."""
from django import forms
from django.test import TestCase
from tasks.forms import UserForm, TeamCreateForm
from tasks.models import User, Team


class TeamFormTestCase(TestCase):
    """Unit tests of the create team form."""

    """ Pre-populates the table with user"""
    fixtures = [
        'tasks/tests/fixtures/other_users.json',
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.form_input = {
            'team_name': 'TestTeam',
            'team_members': [User.objects.get(username='@johndoe'),
                             User.objects.get(username='@janedoe'),
                             User.objects.get(username='@petrapickles'),
                             User.objects.get(username='@peterpickles')]
        }

    def test_form_has_necessary_fields(self):
        form = TeamCreateForm()
        self.assertIn('team_name', form.fields)
        self.assertIn('team_members', form.fields)

        self.assertTrue(isinstance(form.fields['team_members'], forms.ModelMultipleChoiceField))

    def test_valid_team_form(self):
        form = TeamCreateForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_members_uses_form_validation(self):
        """Tests that team members cannot be empty"""
        self.form_input['team_members'] = []
        form = TeamCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = TeamCreateForm(data=self.form_input)
        before_count = Team.objects.count()
        form.save()
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count+1)
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

    def test_duplicate_team_name(self):
        Team.objects.create(team_name='TestTeam')

        form = TeamCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'team_name', 'Team with this Team name already exists.')

