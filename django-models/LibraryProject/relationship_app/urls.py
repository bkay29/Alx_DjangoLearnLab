from django.urls import path
from .views import list_books
from .views import LibraryDetailView

from .views import register
from django.contrib.auth import views as auth_views

urlpatterns = [
    # function-based view
    path('books/', list_books, name='list_books'),

    # class-based view (detail for a library) — DetailView expects a PK by default
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),     
]
