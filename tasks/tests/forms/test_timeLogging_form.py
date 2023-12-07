from django.test import TestCase
from django.utils import timezone
from tasks.forms import TimeEntryForm
from tasks.models import TimeLogging


class TimeEntryFormTest(TestCase):

    def test_valid_time_entry_form(self):
        # Create data for a valid time entry form
        current_time = timezone.now()
        form_data = {
            'start_time': current_time,
            'end_time': current_time + timezone.timedelta(hours=2),
        }

        form = TimeEntryForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_time_entry_form(self):
        # Create data for an invalid time entry form (end_time before start_time)
        current_time = timezone.now()
        form_data = {
            'start_time': current_time,
            'end_time': current_time - timezone.timedelta(hours=2),
        }

        form = TimeEntryForm(data=form_data)

        # Check if the form is not valid
        self.assertFalse(form.is_valid())