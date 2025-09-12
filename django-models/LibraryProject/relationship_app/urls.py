from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (detail for a library) — DetailView expects a PK by default
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
