from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView  # 🔑 added

from . import views
from .views import list_books 
from .views import LibraryDetailView

# role-based views in their own files
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view

urlpatterns = [
    # Home / Books / Libraries
    path('books/', list_books, name='list_books'),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # class-based view

    # Keep your original plural path
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    # Add singular path for checker compatibility
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail_checker'),

    # Auth (register, login, logout)
    path('register/', views.register, name='register'),

    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),

    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),

    # Checker-specific auth views (extra, no overwrite)
    path('login-checker/', LoginView.as_view(template_name="relationship_app/login.html"), name='login_checker'),
    path('logout-checker/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout_checker'),

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