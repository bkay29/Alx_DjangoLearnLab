from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Columns to show in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Filters shown in the right sidebar (or top depending on Django version)
    list_filter = ('publication_year', 'author')

    # Fields that can be searched using the admin search box
    search_fields = ('title', 'author')

# Register the model with the admin site
admin.site.register(Book, BookAdmin)