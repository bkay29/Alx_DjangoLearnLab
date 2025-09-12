from django.shortcuts import render, get_object_or_404
from .models import Book, Library
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Library Project!")

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.views.generic import DetailView


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