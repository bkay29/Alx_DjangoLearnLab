from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

from .models import Book, Library

# ---------------------------
# Home View
# ---------------------------
def home(request):
    return HttpResponse("Welcome to the Library Project!")


# ---------------------------
# Book / Library Views
# ---------------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


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


# ---------------------------
# Registration View
# ---------------------------
def register(request):
    """Simple registration view using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in immediately
            # Optionally, assign user to default group
            member_group, _ = Group.objects.get_or_create(name='Member')
            user.groups.add(member_group)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# ---------------------------
# Role-checking functions
# ---------------------------
def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_librarian(user):
    return user.is_authenticated and user.groups.filter(name='Librarian').exists()

def is_member(user):
    return user.is_authenticated and user.groups.filter(name='Member').exists()


# ---------------------------
# Role-based Views
# ---------------------------
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')