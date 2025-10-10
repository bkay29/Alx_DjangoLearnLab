from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate


from .serializers import UserSerializer, RegisterSerializer
from .models import User


# Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': response.data,
            'token': token.key
   })


# Login - simple email/username + password endpoint returning token
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


# Profile view - get or update the authenticated user
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user
