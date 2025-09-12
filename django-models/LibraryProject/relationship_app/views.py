from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Book
from .models import Library


# Function-based views
def home(request):
    return HttpResponse("Welcome to the Library Project!")


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        try:
            context['books'] = library.books.all()
        except Exception:
            context['books'] = library.book_set.all()
        return context