"Unit tests for the notificaiton model"
from django.test import TestCase
from django.utils import timezone
from tasks.models import Notifications, User, Task, Team

class NotificationsModelTest(TestCase):

    fixtures = [
            
        'tasks/tests/fixtures/other_users.json',
        'tasks/tests/fixtures/default_user.json'
    ]

    def setUp(self):

        self.sender_user = User.objects.get(username='@johndoe')
        self.recipient_user = User.objects.get(username='@janedoe')

        # Create a team
        self.team = Team.objects.create(
            team_name='Test Team',
            team_admin=self.sender_user,
        )

        # Add the recipient user to the team
        self.team.invite_member(self.recipient_user)

        # Create a task associated with the team
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            deadline='2023-12-31',
            priority=2,
            author=self.sender_user,
            team=self.team,
        )

    def test_notifications_model(self):
        # Create a notification
        notification = Notifications.objects.create(
            recipient=self.recipient_user,
            sender=self.sender_user,
            message='Test Message',
            task=self.task
        )

        # Retrieve the notification from the database
        saved_notification = Notifications.objects.get(pk=notification.pk)

        # Test the fields
        self.assertEqual(saved_notification.recipient, self.recipient_user)
        self.assertEqual(saved_notification.sender, self.sender_user)
        self.assertEqual(saved_notification.message, 'Test Message')
        self.assertEqual(saved_notification.task, self.task)

    def test_notifications_ordering(self):
        # Create multiple notifications with different timestamps
        notification1 = Notifications.objects.create(
            recipient=self.recipient_user,
            sender=self.sender_user,
            message='Message 1',
            task=self.task,
            timestamp=timezone.now()
        )

        notification2 = Notifications.objects.create(
            recipient=self.recipient_user,
            sender=self.sender_user,
            message='Message 2',
            task=self.task,
            timestamp=timezone.now() + timezone.timedelta(days=1)
        )

        # Retrieve notifications from the database
        notifications = Notifications.objects.all()

        # Test the ordering
        self.assertEqual(notifications[0], notification2)
        self.assertEqual(notifications[1], notification1)