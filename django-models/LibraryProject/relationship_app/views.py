from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from .models import Book
from .models import Library

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

# Function-based views
def home(request):
    return HttpResponse("Welcome to the Library Project!")


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


def register(request):
    """Simple registration view using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in immediately after successful registration
            login(request, user)
            # Redirect to a page in your project; change 'list_books' to your actual view name if needed
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


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