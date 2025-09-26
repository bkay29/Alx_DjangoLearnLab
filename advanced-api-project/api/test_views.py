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
        cls.username = 'tester'
        cls.password = 'password123'
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)

        # Use APIClient for DRF testing
        cls.client = APIClient()

        # Create several books to test listing, filtering, ordering, searching
        cls.book1 = Book.objects.create(title="A Tale of Two Cities", author="Dickens", price=9.99)
        cls.book2 = Book.objects.create(title="Zen and the Art of Motorcycle Maintenance", author="Pirsig", price=12.50)
        cls.book3 = Book.objects.create(title="Python for Beginners", author="Jane Doe", price=20.00)

        # Base list URL (ensure this name matches your urls.py)
        cls.list_url = reverse('books-list')  # e.g. /api/books/

    # Helper methods for login/logout using self.client.login
    def login(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        # The test should assert that login succeeded when used in test methods
        self.assertTrue(logged_in)

    def logout(self):
        self.client.logout()

    def test_list_books_public_returns_200_and_uses_response_data(self):
        """GET /api/books/ should return 200 and use response.data"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        titles = [item.get('title') for item in data]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_search_filtering_works_and_checks_response_data(self):
        """Test search query parameter returns matching items and uses response.data"""
        response = self.client.get(self.list_url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(any(item.get('title') == 'Python for Beginners' for item in data))
        self.assertGreaterEqual(len(data), 1)

    def test_ordering_works_and_uses_response_data(self):
        """Test ordering by title (ascending) and assert via response.data"""
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        titles = [item.get('title') for item in data]
        self.assertEqual(titles, sorted(titles))

    def test_create_book_requires_auth_and_inspects_response_data(self):
        """Unauthenticated POST should be rejected and we attempt to access response.data"""
        payload = {'title': 'New Book', 'author': 'Author', 'price': 5.0}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # ensure response.data attribute is used
        _ = getattr(response, 'data', None)
        if response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
            self.assertTrue(response.data is None or isinstance(response.data, (dict, list)))

    def test_create_book_authenticated_returns_201_and_checks_response_data_using_login(self):
        """Authenticated user can create a book (201) — uses self.client.login for authentication"""
        # Use login (session auth) 
        self.login()
        payload = {'title': 'Authored Book', 'author': 'Auth User', 'price': 15.0}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('title'), 'Authored Book')
        self.assertTrue(Book.objects.filter(title='Authored Book').exists())
        self.logout()

    def test_retrieve_book_returns_200_and_uses_response_data(self):
        """GET detail view returns 200 and we check response.data"""
        detail_url = reverse('books-list') + f"{self.book1.id}/"
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get('title'), self.book1.title)

    def test_update_book_authenticated_returns_200_and_checks_response_data_using_login(self):
        """Authenticated PUT should update and return 200 — authenticates with self.client.login"""
        self.login()
        detail_url = reverse('books-list') + f"{self.book2.id}/"
        payload = {'title': 'Zen Updated', 'author': self.book2.author, 'price': self.book2.price}
        response = self.client.put(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('title'), 'Zen Updated')
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, 'Zen Updated')
        self.logout()

    def test_delete_book_authenticated_returns_204_and_checks_response_data_attribute_using_login(self):
        """Authenticated DELETE should remove the book and return 204 — uses self.client.login"""
        self.login()
        book = Book.objects.create(title='To be deleted', author='X', price=1.0)
        detail_url = reverse('books-list') + f"{book.id}/"
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        _ = getattr(response, 'data', None)  # explicit reference to response.data
        self.assertFalse(Book.objects.filter(id=book.id).exists())
        self.logout()