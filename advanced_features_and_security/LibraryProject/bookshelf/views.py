from .forms import ExampleForm, BookForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book


def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Use cleaned_data only (validated & normalized)
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            # Example: create a Book safely via ORM
            Book.objects.create(title=title, author=author)
            return redirect('bookshelf:book_list')  # adjust URL name as needed
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


def book_list_view(request):
    q = request.GET.get('q', '').strip()  # raw GET value, but we use ORM filters next
    if q:
        # Safe: the ORM parameterizes queries internally and prevents SQL injection
        books = Book.objects.filter(title__icontains=q)
    else:
        books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books, "query": q})



# Example: list all books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Create a book
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            if request.user.is_authenticated:
                book.added_by = request.user
            book.save()
            return redirect('bookshelf:book_list')  # namespace-safe redirect
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Edit a book
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})


# Delete a book
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# View details
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})
