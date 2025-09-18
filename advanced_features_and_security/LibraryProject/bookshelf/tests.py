from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Book

class PermissionTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="T", author="A")
        ct = ContentType.objects.get_for_model(Book)
        p_view = Permission.objects.get(codename='can_view', content_type=ct)
        p_edit = Permission.objects.get(codename='can_edit', content_type=ct)

        viewers = Group.objects.create(name="Viewers")
        viewers.permissions.add(p_view)

        editors = Group.objects.create(name="Editors")
        editors.permissions.add(p_view, p_edit)

        self.viewer = User.objects.create_user("viewer", password="pass")
        self.viewer.groups.add(viewers)

        self.editor = User.objects.create_user("editor", password="pass")
        self.editor.groups.add(editors)

    def test_viewer_can_view(self):
        self.client.login(username="viewer", password="pass")
        resp = self.client.get(reverse('book_detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_viewer_cannot_edit(self):
        self.client.login(username="viewer", password="pass")
        resp = self.client.get(reverse('book_edit', kwargs={'pk': self.book.pk}))
        self.assertIn(resp.status_code, (302, 403))  # 403 if raise_exception True for logged in user

    def test_editor_can_edit(self):
        self.client.login(username="editor", password="pass")
        resp = self.client.get(reverse('book_edit', kwargs={'pk': self.book.pk}))
        self.assertEqual(resp.status_code, 200)