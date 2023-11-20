"""Unit tests for the Task model."""
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from tasks.models import Task, User

class TaskModelTestCase(TestCase):
    """Unit tests for the Task model."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/default_task.json'
    ]
    
    def setUp(self):
        self.task = Task.objects.get(name='Testing')

        # Make the deadline 1 day from now.
        self.task.deadline = timezone.now() + timedelta(days=1)

    def test_valid_task(self):
        self._assert_task_is_valid()


    def test_name_cannot_be_blank(self):
        self.task.name = ''
        self._assert_task_is_invalid()

    def test_name_can_be_50_characters_long(self):
        self.task.name = 'x' * 50
        self._assert_task_is_valid()

    def test_name_cannot_be_over_50_characters_long(self):
        self.task.name = 'x' * 51
        self._assert_task_is_invalid()


    def test_description_cannot_be_blank(self):
        self.task.description = ''
        self._assert_task_is_invalid()

    def test_description_can_be_5000_characters_long(self):
        self.task.description = 'x' * 5000
        self._assert_task_is_valid()

    def test_description_cannot_be_over_5000_characters_long(self):
        self.task.description = 'x' * 5001
        self._assert_task_is_invalid()

    
    def test_deadline_cannot_be_blank(self):
        self.task.deadline = ''
        self._assert_task_is_invalid()

    def test_deadline_cannot_be_incorrectly_formatted(self):
        self.task.deadline = "16th November 2023"
        self._assert_task_is_invalid()

    def test_deadline_can_be_in_past(self):
        self.task.deadline = "2021-11-16T15:43:22.039Z"
        self._assert_task_is_valid()

    def test_deadline_cannot_contain_invalid_value(self):
        self.task.deadline = "2023-11-40T15:43:22.039Z"
        self._assert_task_is_invalid()


    def test_priority_cannot_be_blank(self):
        self.task.priority = None
        self._assert_task_is_invalid()

    def test_priority_cannot_be_less_than_1(self):
        self.task.priority = 0
        self._assert_task_is_invalid()

    def test_priority_cannot_be_greater_than_5(self):
        self.task.priority = 6
        self._assert_task_is_invalid()

    def test_priority_can_be_1(self):
        self.task.priority = 1
        self._assert_task_is_valid()
    
    def test_priority_can_be_5(self):
        self.task.priority = 5
        self._assert_task_is_valid()


    def test_author_is_type_user(self):
        self.assertTrue(isinstance(self.task.author, User))

    def test_author_cannot_be_invalid_user(self):
        self.task.author = User(username="bad_username")
        self._assert_task_is_invalid()

    def test_author_cannot_be_none(self):
        self.task.author = None
        self._assert_task_is_invalid()
        

    def _assert_task_is_valid(self):
        try:
            self.task.full_clean()
        except ValidationError:
            self.fail('Test task should be valid')

    def _assert_task_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.task.full_clean()