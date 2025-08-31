# Create Operation

from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# Expected output: <Book: 1984 by George Orwell (1949)>

# Retrieve Operation

from bookshelf.models import Book
books = Book.objects.all()
books
# Expected output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>

# Update Operation

from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# Expected output: <Book: Nineteen Eighty-Four by George Orwell (1949)>

# Delete Operation

from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# Expected output: <QuerySet []>