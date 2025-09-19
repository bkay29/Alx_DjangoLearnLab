from rest_framework.generics import ListAPIView
from rest_framework import permissions
import rest_framework.viewsets

from .models import Book
from .serializers import BookSerializer

# The old BookList view for the 'books/' endpoint
class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# The new BookViewSet for full CRUD operations
class BookViewSet(rest_framework.viewsets.ModelViewSet):
    """
    BookViewSet handles list, create, retrieve, update, and destroy for Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # adjust as needed