# Retrieve Operation

from bookshelf.models import Book
# Retrieve all books
books = Book.objects.all()
books
# Expected output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>

book = Book.objects.get(title="1984")
book
# Expected output: <Book: 1984 by George Orwell (1949)>
