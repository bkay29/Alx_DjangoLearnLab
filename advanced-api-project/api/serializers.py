from rest_framework import serializers
from .models import Author, Book
import datetime

# BookSerializer: serializes all Book model fields as required, includes custom validation to prevent publication_year in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'   #serialize all fields of the Book model

    def validate_title(self, value):
        """
        Ensure title is not empty or just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    # Field-level validation for publication_year
    def validate_publication_year(self, value):
        """
        Ensure publication_year is not in the future.
        This uses the local calendar year (datetime.date.today().year).
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value   

# AuthorSerializer: includes the Author 'name' and a nested list of the author's books.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('name', 'books')