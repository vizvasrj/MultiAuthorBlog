# from django.http import response
# from django.urls import reverse
# from django.shortcuts import get_object_or_404, redirect
# from account.models import Profile
from django.utils import translation

def language_change_middleware(get_response):
    # Language Change
    def middleware(request):
        if request.user.is_authenticated:
            translation.activate(request.user.profiles.lang)
        response = get_response(request)
        # print(request.META.get("REMOTE_ADDR"))
        return response
    return middleware

