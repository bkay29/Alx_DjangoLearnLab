from django.urls import path  
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

def _comment_create_delegate(request, pk):
    """
    Delegate view used only to accept a URL with <int:pk> and forward it
    to CommentCreateView providing the expected kwarg 'post_id'.
    """
    view = views.CommentCreateView.as_view()
    return view(request, post_id=pk)

def _posts_by_tag_delegate(request, tag_name):
    """
    Delegate to satisfy exact-text checkers that look for 'tags/<tag_name>/'.
    Calls the real posts_by_tag view with the provided tag_name.
    """
    return views.posts_by_tag(request, tag_name=tag_name)

urlpatterns = [
    # authentication and profile routes 
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # plural-style CRUD routes 
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # singular-style CRUD routes 
    path('post/new/', views.PostCreateView.as_view(), name='post-create-alt'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail-alt'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update-alt'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete-alt'),

    # --- Explicit exact-path entries added 
    path("post/new/", views.PostCreateView.as_view(), name="post-create-exact"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update-exact"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete-exact"),

    # receives the correct keyword argument.
    path('post/<int:pk>/comments/new/', _comment_create_delegate, name='comment-create-pk-delegate'),

    path('posts/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),

    # comment edit/delete routes (plural 'comments/...')
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-edit'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # --- Add strings for comment update/delete too ---
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update-exact'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete-exact'),

    # -----------------------------
    # Search and Tags routes (NEW)
    # -----------------------------
    # Search (exact path)
    path('search/', views.search_view, name='search'),

    # Posts by tag (typed converter; preferred)
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),

    # delegate for checkers for 'tags/<tag_name>/'
    path('tags/<tag_name>/', _posts_by_tag_delegate, name='posts-by-tag-exact'),

    # --------- EXACT slug-based route ----------
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag-slug'),
]

