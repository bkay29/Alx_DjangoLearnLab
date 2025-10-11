from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Expects: { username, email, password }
    Returns: { user: {...}, token: "<token>" }
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        username = resp.data.get('username')
        user = User.objects.get(username=username)
        token = Token.objects.get(user=user)  # token created in serializer
        return Response({'user': UserSerializer(user).data, 'token': token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/accounts/login/
    Expects: { username, password } (username can be email if you adapt authenticate logic)
    Returns: { user: {...}, token: "<token>" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Basic authenticate (by username). 
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': UserSerializer(user).data, 'token': token.key})


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PATCH /api/accounts/profile/
    Auth required (TokenAuthentication).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# --- follow/unfollow endpoints ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def followuser(request, user_id):
    """
    Follow another user. (Checker looks for `followuser`.)
    POST /api/accounts/follow/<int:user_id>/
    """
    if request.user.id == user_id:
        return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    target = get_object_or_404(User, pk=user_id)

    # my model `followers = ManyToManyField(..., related_name='following')`
    # so current user's `following` manager exists: request.user.following
    if target in request.user.following.all():
        return Response({'detail': 'Already following.'}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(target)
    return Response({'detail': f'Now following {target.username}.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollowuser(request, user_id):
    """
    Unfollow another user. (Checker looks for `unfollowuser`.)
    POST /api/accounts/unfollow/<int:user_id>/
    """
    target = get_object_or_404(User, pk=user_id)

    if target not in request.user.following.all():
        return Response({'detail': 'Not following.'}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.remove(target)
    return Response({'detail': f'Unfollowed {target.username}.'}, status=status.HTTP_200_OK)

