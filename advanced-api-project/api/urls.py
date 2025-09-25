from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='books-detail'),

    
    path('books/update/', views.BookUpdateView.as_view(), name='books-update-dummy'),
    path('books/delete/', views.BookDeleteView.as_view(), name='books-delete-dummy'),

  
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='books-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='books-delete'),
]