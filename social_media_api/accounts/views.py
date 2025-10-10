from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

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
