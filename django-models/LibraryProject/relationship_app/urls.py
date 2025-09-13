from django.urls import path
from .views import list_books
from .views import LibraryDetailView

from . import views
from .views import register
from django.contrib.auth import views as auth_views

from . import admin_view
from . import librarian_view
from . import member_view

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (detail for a library) — DetailView expects a PK by default
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),     
]

urlpatterns = [
    path('role/admin/', admin_view.admin_view, name='admin_view'),
    path('rolelibrarian/', librarian_view.librarian_view, name='librarian_view'),
    path('role/member/', member_view.member_view, name='member_view'),
]