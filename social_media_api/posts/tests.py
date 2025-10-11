from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Post
from django.utils import timezone

User = get_user_model()

class FeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        self.u3 = User.objects.create_user(username='u3', password='pass')

        # u1 follows u2 only
        self.u1.following.add(self.u2)

        # create posts: older first, then newer
        self.p_old = Post.objects.create(author=self.u2, content='old post')
        self.p_new = Post.objects.create(author=self.u2, content='new post')

        self.client = APIClient()
        self.client.force_authenticate(user=self.u1)

    def test_feed_returns_posts_from_followed_users_ordered(self):
        resp = self.client.get('/api/posts/feed/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # newest should be first
        self.assertEqual(data[0]['content'], 'new post')
        self.assertEqual(data[1]['content'], 'old post')
        # posts from u3 (not followed) should not be present

