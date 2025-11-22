from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow access if the object belongs to the requesting user
        return obj.owner == request.user

class IsAdminOrReadOnly(BasePermission):
    """
    Allow only admins to edit (POST/PUT/DELETE), but everyone else can read (GET/HEAD/OPTIONS).
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
