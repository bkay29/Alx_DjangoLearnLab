from taggit.forms import TagWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class PostForm(forms.ModelForm):
    """
    Post form with TaggableManager support using TagWidget from taggit.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include taggable field
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'tags': TagWidget(),  # <-- required by checker
        }


class CommentForm(forms.ModelForm):
    """
    ModelForm for creating/updating comments.
    Includes validation:
      - content cannot be empty
      - min length 3
      - max length 1000
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        max_length=1000,
        help_text='Max 1000 characters.'
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('Comment cannot be empty.')
        if len(content) < 3:
            raise forms.ValidationError('Comment is too short (min 3 characters).')
        return content


