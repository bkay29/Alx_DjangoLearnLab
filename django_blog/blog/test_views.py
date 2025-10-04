from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

class PostPermissionTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='auth', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.post = Post.objects.create(title='T', content='C', author=self.author)

    def test_only_author_can_edit(self):
        self.client.login(username='other', password='pass')
        resp = self.client.get(reverse('blog:post-update', args=[self.post.pk]))
        self.assertIn(resp.status_code, (302, 403))  # either redirect or forbidden

    def test_author_can_edit(self):
        self.client.login(username='auth', password='pass')
        resp = self.client.get(reverse('blog:post-update', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)
