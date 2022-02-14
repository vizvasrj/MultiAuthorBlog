from rest_framework import permissions
from django.contrib.auth.models import User

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is permissions.SAFE_METHODS:
            return True
        else:
            return User.objects.get(user=request.user) in obj.edited_by.all()