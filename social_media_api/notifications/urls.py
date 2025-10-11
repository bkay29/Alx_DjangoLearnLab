from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.list_notifications, name='notifications'),  # /notifications/
    path('<int:pk>/mark-read/', views.mark_as_read, name='notification-mark-read'),
]
