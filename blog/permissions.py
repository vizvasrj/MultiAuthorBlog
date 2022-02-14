from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import permissions
from account.models import Profile
from rest_framework.exceptions import NotAuthenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is permissions.SAFE_METHODS:
            return True
        else:
            # print('Here')
            try:
                return obj.author == Profile.objects.get(user=request.user)
            except TypeError:
                raise NotAuthenticated(
                    "Try to login again"
                )
