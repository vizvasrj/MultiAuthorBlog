# from django.http import response
# from django.urls import reverse
# from django.shortcuts import get_object_or_404, redirect
# from account.models import Profile
from django.utils import translation
import requests

def language_change_middleware(get_response):
    # Language Change
    def middleware(request):
        if request.user.is_authenticated:
            translation.activate(request.user.profiles.lang)
        response = get_response(request)
        ip = request.META.get("REMOTE_ADDR")
        curl = requests.get(f'http://ip-api.com/csv/{ip}?fields=countryCode')
        text = curl.text
        country_code = text.split('\n')[0]
        if country_code == 'IN':
            translation.activate('hi')
        elif country_code == 'DE':
            translation.activate('de')
        else:
            translation.activate('fr')
        print(text, country_code, "text and &&& country code")
        return country_code
    return middleware
