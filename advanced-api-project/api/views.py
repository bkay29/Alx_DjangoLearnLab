from rest_framework import generics, filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend


class BookListView(generics.ListAPIView):
    """
    GET /api/books/  -> list all books
    Public read-only access allowed.
    Supports:
      - Filtering by title, author, publication_year via query params
      - Search on title and author via ?search=
      - Ordering by title, publication_year (and published_date if present) via ?ordering=
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # enable django-filter, DRF search, and ordering
    filter_backends = [
        DjangoFilterBackend,   # django_filters integration (for ?title=... etc)
        filter.SearchFilter,          # for ?search=
        filter.OrderingFilter,        # for ?ordering=
    ]

    # fields exposed for simple filtering: ?title=...&author=...&publication_year=...
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']   # adjust to real fields in Book
    ordering_fields = ['title', 'publication_year', 'published_date', 'author', 'id']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<int:pk>/  -> retrieve a single book by id
    Public read-only access allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/  -> create a new book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save new book and attach user if model supports it.
        """
        try:
            serializer.save(created_by=self.request.user)
        except TypeError:
            serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<int:pk>/update/  -> update a book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        try:
            serializer.save(updated_by=self.request.user)
        except TypeError:
            serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<int:pk>/delete/  -> delete a book
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]