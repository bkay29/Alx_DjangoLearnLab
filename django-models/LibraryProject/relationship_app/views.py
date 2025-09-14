from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import Group
from .models import Book
from .models import Library   
from .forms import BookForm  # make sure you have a BookForm for adding/editing books


# ---------------------------
# Home View
# ---------------------------
def home(request):
    return HttpResponse("Welcome to the Library Project!")


# ---------------------------
# Book / Library Views
# ---------------------------

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
    # If you want to keep namespaced templates, you can add both options:
    # return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view: Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'   
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        # safer way: handle both related_name=books and default book_set
        context['books'] = getattr(library, 'books', library.book_set).all()
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


# ---------------------------
# Book Management Views with Permissions
# ---------------------------

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})