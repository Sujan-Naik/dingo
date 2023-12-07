from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from tasks.models import TimeLogging, User, Task

class TimeLoggingModelTest(TestCase):

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/default_team.json',
        'tasks/tests/fixtures/default_task.json',
    ]

    def setUp(self):
        # Create a user and a task for testing
        self.user = User.objects.get(username='@johndoe')
        self.task = Task.objects.get(name='Testing')

    def test_valid_time_logging_entry(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=2)

        # Create a valid TimeLogging entry
        time_logging = TimeLogging.objects.create(
            user=self.user,
            task=self.task,
            start_time=start_time,
            end_time=end_time,
        )

        # Check if the duration_minutes field is calculated correctly
        self.assertEqual(time_logging.duration_minutes, (end_time - start_time).total_seconds() // 60)

    def test_invalid_time_logging_entry(self):
        # Try to create an invalid TimeLogging entry (end_time before start_time)
        start_time = timezone.now()
        end_time = start_time - timezone.timedelta(hours=2)

        with self.assertRaises(ValidationError):
            TimeLogging.objects.create(
                user=self.user,
                task=self.task,
                start_time=start_time,
                end_time=end_time,
            )


    def test_duration_calculation(self):
        # Create a TimeLogging entry with start_time and end_time
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=2)
        time_logging = TimeLogging.objects.create(
            user=self.user,
            task=self.task,
            start_time=start_time,
            end_time=end_time,
        )

        # Check if the duration is calculated correctly after saving
        self.assertEqual(time_logging.duration, end_time - start_time)

