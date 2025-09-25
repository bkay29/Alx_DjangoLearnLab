from django.urls import path
from . import views

urlpatterns = [
    # list & detail (public)
    path('books/', views.BookListView.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='books-detail'),

    # ----- Explicit literal routes 
    # both with and without trailing slash to be ultra-explicit
    path('books/update', views.BookUpdateView.as_view(), name='books-update-no-slash'),
    path('books/update/', views.BookUpdateView.as_view(), name='books-update-dash-slash'),

    path('books/delete', views.BookDeleteView.as_view(), name='books-delete-no-slash'),
    path('books/delete/', views.BookDeleteView.as_view(), name='books-delete-dash-slash'),
    # --------------------------------------------------------------------

    # functional routes that actually accept a pk for update/delete operations
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='books-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='books-delete'),
]