from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm

# Class-based view imports
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment


def register_view(request):
    """Handle user registration (GET shows form, POST creates user)."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # sign in immediately after registration
            messages.success(request, "Registration successful.")
            return redirect('blog:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    Allow authenticated users to view and edit profile details.
    Handles POST requests to update user information (email, first_name, last_name).
    """
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('blog:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})


# ------------------------------------
# Post CRUD views (class-based views)
# ------------------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # blog/templates/blog/post_list.html
    context_object_name = 'posts'
    paginate_by = 10  # optional


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # blog/templates/blog/post_detail.html


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new post. Only authenticated users may create posts.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'  # assumes a 'login' named URL exists

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing post. Only the post's author may update it.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def test_func(self):
        # Ensures only the author can edit
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        # Provide a friendly message and default behavior
        messages.error(self.request, "You do not have permission to edit this post.")
        return super().handle_no_permission()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a post. Only the post's author may delete it.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def test_func(self):
        # Ensures only the author can delete
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this post.")
        return super().handle_no_permission()


# ------------------------------------
# Comment views (CRUD)
# ------------------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a comment for a given post (URL must provide post_id).
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comments/comment_form.html'  # create this template
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        # Ensure the post exists and store it on the view
        self.post = get_object_or_404(Post, pk=kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set author and related post before saving
        form.instance.author = self.request.user
        form.instance.post = self.post
        messages.success(self.request, "Comment posted.")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the post detail page
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing comment. Only the comment author may update.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comments/comment_form.html'
    login_url = 'login'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this comment.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.get_object().post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an existing comment. Only the comment author may delete.
    """
    model = Comment
    template_name = 'blog/comments/comment_confirm_delete.html'
    login_url = 'login'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this comment.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.get_object().post.pk})


def comment_list(request, post_id):
    """
    Optional explicit view to list comments for a post.
    """
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(request, 'blog/comments/comment_list.html', {'post': post, 'comments': comments})
