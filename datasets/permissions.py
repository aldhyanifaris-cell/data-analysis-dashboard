"""
Datasets Permissions.
"""
from rest_framework import permissions

class IsDatasetOwnerOrSharedOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.is_public:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if obj.owner == request.user or request.user.is_staff:
            return True
        if obj.shares.filter(shared_with=request.user).exists():
            return True
        return False
