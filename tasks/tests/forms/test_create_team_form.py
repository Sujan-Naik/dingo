"""Unit tests of the create team form."""
from django import forms
from django.test import TestCase
from tasks.forms import UserForm
from tasks.models import User

class TeamFormTestCase(TestCase):
    """Unit tests of the create team form."""

    fixtures = [
        'tasks/tests/fixtures/default_team.json'
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        user = User.objects.get(username='@johndoe')
        self.form_input = {
            'team_name': 'TestTeam',
            'team_members': user
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('team_name', form.fields)
        self.assertIn('team_members', form.fields)

        self.assertTrue(isinstance(form.fields['team_members'], forms.ModelMultipleChoiceField))

    def test_valid_team_form(self):
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_name_uses_model_validation(self):
        self.form_input['team_name'] = ''
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='@johndoe')
        form = UserForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, '@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
