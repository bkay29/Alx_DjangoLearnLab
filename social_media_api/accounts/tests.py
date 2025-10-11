from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class FollowUnfollowTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')

        self.client = APIClient()
        self.client.force_authenticate(user=self.u1)

    def test_follow_and_unfollow(self):
        # follow
        resp = self.client.post(f'/api/accounts/follow/{self.u2.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(self.u2, self.u1.following.all())

        # cannot follow again
        resp2 = self.client.post(f'/api/accounts/follow/{self.u2.id}/')
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

        # unfollow
        resp3 = self.client.post(f'/api/accounts/unfollow/{self.u2.id}/')
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.u2, self.u1.following.all())

