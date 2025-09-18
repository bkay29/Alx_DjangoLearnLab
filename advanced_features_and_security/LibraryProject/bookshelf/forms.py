from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class ExampleForm(forms.Form):
    # Example safe fields — adapt to your app's needs
    title = forms.CharField(max_length=200, required=True)
    author = forms.CharField(max_length=100, required=False)
    query = forms.CharField(max_length=100, required=False)

    def clean_title(self):
        data = self.cleaned_data.get('title', '').strip()
        # additional validation or normalization can go here
        return data
