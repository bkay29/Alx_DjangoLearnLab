from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

# -------------------------
# Read endpoints (public)
# -------------------------
class BookListAPIView(generics.ListAPIView):
    """
    GET /api/books/  -> list all books
    Read-only for unauthenticated users (AllowAny).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    # Optional: enable search & ordering for convenience
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author']          # adjust to real fields
    ordering_fields = ['title', 'published_date']

class BookDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/books/<int:pk>/  -> retrieve a single book by id
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------------
# Write endpoints (authenticated only)
# -----------------------------------
class BookCreateAPIView(generics.CreateAPIView):
    """
    POST /api/books/create/  -> create a new book
    Only authenticated users allowed as required by the task.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Example: attach a user if model supports owner/created_by field.
        This tries to save created_by if present; otherwise it just saves normally.
        """
        try:
            serializer.save(created_by=self.request.user)
        except TypeError:
            # model doesn't accept created_by in serializer.save(), fall back
            serializer.save()


class BookUpdateAPIView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<int:pk>/update/  -> update existing book
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # optionally record who updated it if your model supports that
        try:
            serializer.save(updated_by=self.request.user)
        except TypeError:
            serializer.save()


class BookDeleteAPIView(generics.DestroyAPIView):
    """
    DELETE /api/books/<int:pk>/delete/  -> delete a book
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]