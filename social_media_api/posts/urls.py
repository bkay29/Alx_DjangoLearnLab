from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, feed, like_post, unlike_post

app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('feed/', feed, name='feed'),
    path('posts/<int:pk>/like/', like_post, name='post-like'),
    path('posts/<int:pk>/unlike/', unlike_post, name='post-unlike'),
    path('', include(router.urls)),
]


