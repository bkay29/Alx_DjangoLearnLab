from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()

class NotificationsEndpointTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.u1)

    def test_list_notifications(self):
        # create a notification directly
        Notification.objects.create(recipient=self.u1, actor=self.u1, verb='test')
        resp = self.client.get('/api/notifications/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.json()), 1)
