from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm

# Imports for class-based CRUD views
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Import the Post model
from .models import Post


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


# ----------------------------
# Post CRUD class-based views
# ----------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # blog/templates/blog/post_list.html
    context_object_name = 'posts'
    paginate_by = 10  


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # blog/templates/blog/post_detail.html


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'  # blog/templates/blog/post_form.html
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'  # you have a 'login' named URL

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def test_func(self):
        # Only the author can update
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit this post.")
        return super().handle_no_permission()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
    login_url = 'login'

    def test_func(self):
        # Only the author can delete
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this post.")
        return super().handle_no_permission()
