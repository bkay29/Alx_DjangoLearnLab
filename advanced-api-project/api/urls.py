from django.urls import path
from . import views

urlpatterns = [
    # list & detail (public)
    path('books/', views.BookListView.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='books-detail'),


    # create route (both forms)
    path('books/create', views.BookCreateView.as_view(), name='books-create-no-slash'),
    path('books/create/', views.BookCreateView.as_view(), name='books-create'),

    # update/delete literal forms (both forms)
    path('books/update', views.BookUpdateView.as_view(), name='books-update-no-slash'),
    path('books/update/', views.BookUpdateView.as_view(), name='books-update-dash-slash'),

    path('books/delete', views.BookDeleteView.as_view(), name='books-delete-no-slash'),
    path('books/delete/', views.BookDeleteView.as_view(), name='books-delete-dash-slash'),
    # --------------------------------------------------------------------

    # functional routes that actually accept a pk for update/delete operations
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='books-update-pk'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='books-delete-pk'),
]