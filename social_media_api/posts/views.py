from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from notifications.utils import create_notification
from django.shortcuts import get_object_or_404


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for Post.
    - list, retrieve open to all (IsAuthenticatedOrReadOnly)
    - create requires authentication and sets author = request.user
    - update/delete allowed only for the post author (IsOwnerOrReadOnly)
    - supports search by title/content and pagination
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']  # search/filter capability
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Comment.
    - comment creation requires authentication and sets author = request.user
    - update/delete allowed only for the comment author
    - pagination and optional search by content
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------
# Feed view 
# ---------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    """
    GET /api/posts/feed/
    Returns posts from users that the current user follows,
    ordered by creation date (most recent first).

    Uses User model's reverse related manager `following`:
      - followers = ManyToManyField('self', related_name='following')
      - therefore: request.user.following.all() returns users the request.user follows
    """
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    """
    POST /api/posts/posts/<int:pk>/like/
    Creates a Like (if not exists) and generates a Notification for the post author.
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.author == user:
        return Response({'detail': 'Cannot like your own post.'}, status=status.HTTP_400_BAD_REQUEST)

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)

    # create notification to post author (if not liking self)
    if post.author != user:
        create_notification(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target=post
        )

    return Response({'detail': 'Post liked.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    """
    POST /api/posts/posts/<int:pk>/unlike/
    Removes a Like (if exists). Does NOT delete historical notifications by default.
    """
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    deleted, _ = Like.objects.filter(user=user, post=post).delete()
    if not deleted:
        return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)

    # optional.
    return Response({'detail': 'Like removed.'}, status=status.HTTP_200_OK)


