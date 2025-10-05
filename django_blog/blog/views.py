from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q

from .models import Post, Comment
from taggit.models import Tag  # <-- taggit's Tag model


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('blog:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('blog:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})


# ------------------------------
# Post CRUD views
# ------------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Handle tags (taggit expects a list of strings)
        tags_str = form.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        self.object.tags.set(tag_names)  # taggit auto-creates tags
        messages.success(self.request, "Post created successfully.")
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        tags_str = form.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        self.object.tags.set(tag_names)
        messages.success(self.request, "Post updated successfully.")
        return response

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this post.")
        return super().handle_no_permission()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this post.")
        return super().handle_no_permission()


# ------------------------------
# Comment CRUD views
# ------------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comments/comment_form.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        messages.success(self.request, "Comment posted.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comments/comment_form.html'
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this comment.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.get_object().post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comments/comment_confirm_delete.html'
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this comment.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.get_object().post.pk})


def comment_list(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(request, 'blog/comments/comment_list.html', {'post': post, 'comments': comments})


# ------------------------------
# Search and tag views
# ------------------------------

def search_view(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'query': query, 'posts': posts})


def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name__iexact=tag_name)
    posts = Post.objects.filter(tags__name__iexact=tag_name)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})

