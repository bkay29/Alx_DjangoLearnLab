# relationship_app/query_samples.py
import os
import sys
import django

# Ensure project root is on path so this script can be run directly
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# IMPORTANT: replace 'LibraryProject.settings' with your project's settings module if different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def seed_sample_data():
    """Create sample data if DB is empty — helpful for testing the sample queries."""
    if Author.objects.exists():
        return

    a1 = Author.objects.create(name='Chinua Achebe')
    a2 = Author.objects.create(name="Ngugi wa Thiong'o")

    b1 = Book.objects.create(title='Things Fall Apart', author=a1)
    b2 = Book.objects.create(title='No Longer at Ease', author=a1)
    b3 = Book.objects.create(title='Petals of Blood', author=a2)

    lib = Library.objects.create(name='Central Library')
    lib.books.add(b1, b2, b3)

    Librarian.objects.create(name='Grace', library=lib)
    print("Seeded sample data.")

def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")
        return

    print(f"Books in library '{library.name}':")
    for book in library.books.all():
        print(f"- {book.title} (author: {book.author.name})")

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"No author found with name: {author_name}")
        return

    qs = Book.objects.filter(author=author)
    print(f"Books by '{author.name}':")
    for b in qs:
        print(f"- {b.title}")

def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")
        return

    # Access the OneToOne reverse relation: library.librarian
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for '{library.name}': {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to library '{library.name}'")
        return

    print(f"Librarian for '{library.name}': {librarian.name}")

if __name__ == '__main__':
    # Seed (only if empty) and run sample queries
    seed_sample_data()
    print()
    list_books_in_library('Central Library')
    print()
    books_by_author('Chinua Achebe')
    print()
    get_librarian_for_library('Central Library')