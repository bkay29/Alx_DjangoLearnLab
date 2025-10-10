from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow read to anyone, but write (PUT/PATCH/DELETE)
    only if request.user is the object's author (owner).
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # must have 'author' attribute
        return getattr(obj, 'author', None) == request.user
