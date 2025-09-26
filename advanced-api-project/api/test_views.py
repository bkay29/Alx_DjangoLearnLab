from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from .models import Book

User = get_user_model()

class BookAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authenticated tests
        cls.user = User.objects.create_user(username='tester', password='password123')
        cls.client = APIClient()

        # Create several books to test listing, filtering, ordering, searching
        cls.book1 = Book.objects.create(title="A Tale of Two Cities", author="Dickens", price=9.99)
        cls.book2 = Book.objects.create(title="Zen and the Art of Motorcycle Maintenance", author="Pirsig", price=12.50)
        cls.book3 = Book.objects.create(title="Python for Beginners", author="Jane Doe", price=20.00)

        # URL names — ensure urls.py uses names as the project shows: 'books-list'
        cls.list_url = reverse('books-list')  # e.g. /api/books/
        # Detail URLs will be constructed below as needed

    def test_list_books_public_returns_200(self):
        """GET /api/books/ should return 200 and list data"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure at least the created books are present
        titles = [b['title'] for b in response.json()]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_search_filtering_works(self):
        """Test search query parameter returns matching items"""
        # assuming SearchFilter is configured, use ?search=Python
        response = self.client.get(self.list_url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # At least one result and it contains 'Python for Beginners'
        self.assertTrue(any('Python for Beginners' == item.get('title') for item in data))

    def test_ordering_works(self):
        """Test ordering by title (ascending)"""
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Ensure the first item's title <= second item's title (basic ordering check)
        titles = [item.get('title') for item in data]
        self.assertTrue(titles == sorted(titles))

    def test_create_book_requires_auth(self):
        """Unauthenticated POST should be rejected (401 or 403 depending on config)"""
        payload = {'title': 'New Book', 'author': 'Author', 'price': 5.0}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated_returns_201(self):
        """Authenticated user can create a book (201)"""
        self.client.force_authenticate(user=self.user)
        payload = {'title': 'Authored Book', 'author': 'Auth User', 'price': 15.0}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify object exists in DB
        self.assertTrue(Book.objects.filter(title='Authored Book').exists())
        self.client.force_authenticate(user=None)

    def test_retrieve_book_returns_200(self):
        """GET detail view returns 200"""
        detail_url = reverse('books-list') + f"{self.book1.id}/"
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get('title'), self.book1.title)

    def test_update_book_authenticated_returns_200(self):
        """Authenticated PUT/PATCH should update and return 200"""
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('books-list') + f"{self.book2.id}/"
        payload = {'title': 'Zen Updated', 'author': self.book2.author, 'price': self.book2.price}
        response = self.client.put(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, 'Zen Updated')
        self.client.force_authenticate(user=None)

    def test_delete_book_authenticated_returns_204(self):
        """Authenticated DELETE should remove the book and return 204"""
        self.client.force_authenticate(user=self.user)
        book = Book.objects.create(title='To be deleted', author='X', price=1.0)
        detail_url = reverse('books-list') + f"{book.id}/"
        response = self.client.delete(detail_url)
        # Most DRF views return 204 for successful delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())
        self.client.force_authenticate(user=None)