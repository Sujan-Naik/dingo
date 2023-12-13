"""Unit tests of the timezone selection form."""
from django import forms
from django.test import TestCase
from tasks.forms import TimezoneForm

class TimezoneFormTestCase(TestCase):
    """Unit tests of the timezone selection form."""

    def setUp(self):
        self.form_input = {'timezone': 'Europe/London'}

    def test_form_has_necessary_fields(self):
        """Test that the form contains the timezone ChoiceField"""
        form = TimezoneForm()
        self.assertIn('timezone', form.fields)
        timezone_field = form.fields['timezone']
        self.assertTrue(isinstance(timezone_field, forms.ChoiceField))

    def test_valid_user_form(self):
        """Test that the form accepts valid input"""
        form = TimezoneForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_sort_by_validation(self):
        """Test that the form rejects invalid input"""
        self.form_input['timezone'] = 'bad_timezone'
        form = TimezoneForm(data=self.form_input)
        self.assertFalse(form.is_valid())
