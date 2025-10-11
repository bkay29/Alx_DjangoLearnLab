from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    followuser,
    unfollowuser,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', followuser, name='followuser'),
    path('unfollow/<int:user_id>/', unfollowuser, name='unfollowuser'),
]
