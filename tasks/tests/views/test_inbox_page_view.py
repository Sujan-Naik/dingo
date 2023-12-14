from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Notifications

class InboxPageViewTest(TestCase):
    def setUp(self):
        # Create a test user
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Create some test notifications for the user
        Notifications.objects.create(recipient=self.user, sender=self.user, message='Test Notification 1')
        Notifications.objects.create(recipient=self.user, sender=self.user, message='Test Notification 2')

    def test_inbox_page_view(self):
        # Access the inbox page
        response = self.client.get(reverse('inbox'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the notifications are displayed in the response context
        self.assertIn('notifications', response.context)

        # Check that the number of notifications matches the number created in setUp
        notifications_count = Notifications.objects.filter(recipient=self.user).count()
        self.assertEqual(len(response.context['notifications']), notifications_count)

        # Check that the rendered HTML contains the notification messages
        for notification in Notifications.objects.filter(recipient=self.user):
            self.assertContains(response, notification.message)
