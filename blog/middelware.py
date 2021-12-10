# from django.http import response
# from django.urls import reverse
# from django.shortcuts import get_object_or_404, redirect
# from account.models import Profile
from django.utils import translation
import requests
import datetime
from django.conf import settings


def language_change_middleware(get_response):
    # Cookei set
    def set_cookie(response, key, value, days_expire=7):
        if days_expire is None:
            max_age = 365 * 24 * 60 * 60    # one year
        else:
            max_age = days_expire * 60
        expires = datetime.datetime.strftime(
            datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        response.set_cookie(
            key,
            value,
            max_age=max_age,
            expires=expires,
            secure=settings.SESSION_COOKIE_SECURE or None,
        )
    
    
    # Language Change
    def middleware(request):
        if request.user.is_authenticated:
            translation.activate(request.user.profiles.lang)
        response = get_response(request)

        # get cookie 
        value = request.COOKIES.get('cookie_name_user')
        print(value, "BEFORE ")
        if value is None:
            print('value is none')
            # Cookie is not set
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            curl = requests.get(f'http://ip-api.com/csv/{ip}?fields=countryCode')
            text = curl.text
            country_code = text.split('\n')[0]

            # response.set_cookie('cookie_name', country_code)
            # this function will be used to make cookie
            set_cookie(response, 'cookie_name_user', country_code, 1)
        # # OR
        value = request.COOKIES.get('cookie_name_user')
        if value == 'IN':
            translation.activate('hi')
        elif value == 'DE':
            translation.activate('de')
        elif value == 'US':
            translation.activate('en')
        elif value == 'ES':
            translation.activate('es')
        # translation.activate(value)
        print(value, "VAUE after SET COKKIE")

        # try:
        #     value = request.COOKIES['cookie_name']
        # except KeyError:
        #     print("Key Error")


        return response
    return middleware

