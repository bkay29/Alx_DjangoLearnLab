from django.urls import path
from . import views

urlpatterns = [
    # function-based view
    path('books/', views.list_books, name='list_books'),

    # class-based view (detail for a library) — DetailView expects a PK by default
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
