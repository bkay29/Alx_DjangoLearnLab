from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikesNotificationsTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(author=self.u2, title='t', content='c')

        self.client = APIClient()
        self.client.force_authenticate(user=self.u1)

    def test_like_creates_like_and_notification(self):
        resp = self.client.post(f'/api/posts/posts/{self.post.pk}/like/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.u1, post=self.post).exists())

        # Notification created for post author
        self.assertTrue(Notification.objects.filter(recipient=self.u2, actor=self.u1, verb__icontains='liked').exists())

    def test_unlike_removes_like(self):
        self.client.post(f'/api/posts/posts/{self.post.pk}/like/')
        resp = self.client.post(f'/api/posts/posts/{self.post.pk}/unlike/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Like.objects.filter(user=self.u1, post=self.post).exists())
