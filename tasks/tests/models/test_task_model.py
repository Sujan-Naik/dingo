"""Unit tests for the Task model."""
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from tasks.models import Task

class TaskModelTestCase(TestCase):
    """Unit tests for the Task model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/default_task.json'
    ]
    def setUp(self):
        self.task = Task.objects.get(name='Testing')

        # Make the deadline 1 day from now, so that the task is valid.
        self.task.deadline = timezone.now() + timedelta(days=1)

    def test_valid_task(self):
        self._assert_task_is_valid()

    def test_priority_cannot_be_blank(self):
        self.task.priority = None
        self._assert_task_is_invalid()

    def test_priority_cannot_be_less_than_1(self):
        self.task.priority = 0
        self._assert_task_is_invalid()

    def test_priority_cannot_be_greater_than_5(self):
        self.task.priority = 6
        self._assert_task_is_invalid()

    def test_priority_can_be_5(self):
        self.task.priority = 5
        self._assert_task_is_valid()


    def _assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except ValidationError:
            self.fail('Test task should be valid')

    def _assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()