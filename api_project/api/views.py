from rest_framework import generics, permissions
import rest_framework.viewsets

from .models import Book
from .serializers import BookSerializer

# Keep the old BookList view for 'books/' endpoint
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Apply permissions (must be authenticated to see this list)
    permission_classes = [permissions.IsAuthenticated]

# Add the new BookViewSet for full CRUD operations
class BookViewSet(rest_framework.viewsets.ModelViewSet):
    """
    BookViewSet handles list, create, retrieve, update, and destroy for Book.
    Requires authentication for access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Restrict access — only authenticated users can CRUD books
    permission_classes = [permissions.IsAuthenticated]