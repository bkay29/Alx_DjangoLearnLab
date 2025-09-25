from django.urls import path
from . import views

urlpatterns = [
    # Read
    path('books/', views.BookListAPIView.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='books-detail'),
    
    # Write
    # create is reachable at /api/books/create/ (POST)
    path('books/create/', views.BookCreateAPIView.as_view(), name='books-create'),
    path('books/<int:pk>/update/', views.BookUpdateAPIView.as_view(), name='books-update'),
    path('books/<int:pk>/delete/', views.BookDeleteAPIView.as_view(), name='books-delete'),
]