from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# role-based views in their own files
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view

urlpatterns = [
    # Home / Books / Libraries
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Auth (register, login, logout)
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='relationship_app/logout.html'
    ), name='logout'),

    # Role-based views
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    # ---------------------------
    # Secured Book Management URLs
    # ---------------------------
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]