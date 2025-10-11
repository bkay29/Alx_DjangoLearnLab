from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """
    GET /api/notifications/
    Returns notifications for the authenticated user with unread first (ordered by timestamp).
    """
    qs = request.user.notifications.all().order_by('-timestamp')
    serializer = NotificationSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, pk):
    n = get_object_or_404(Notification, pk=pk, recipient=request.user)
    n.unread = False
    n.save()
    return Response({'detail': 'Marked as read.'})
