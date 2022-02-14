from django.http import response
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser


def subdomain_course_middleware(get_reaponse):
    """
    Subdomain form username
    """
    def middleware(request):
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # get username for the given subdomain
            user = get_object_or_404(User, username=host_parts[0])
            user_url = reverse(
                'user_detail',
                args=[user.username]
            )
            # redirect current request to the user_detail view
            url = '{}://{}{}'.format(
                request.scheme,
                '.'.join(host_parts[1:]),
                user_url
            )
            return redirect(url)
        response = get_reaponse(request)
        return response
    return middleware


class JWTAuthenticationMiddleware(object):
    # print("a")
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda:self.__class__.get_jwt_user(request))
        # print(request.user)
        return self.get_response(request)


    # def process_request(self, request):
    #     request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

        

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        # print(request.user)
        # user = get_user(request)
        # user = AnonymousUser()
        try:
            bearer = request.headers
            try:
                s = bearer['Authorization']
                access_token = s.split(' ')[1]
            except KeyError:
                access_token = request.COOKIES['jwtt']
        except KeyError:
            user = AnonymousUser()
            # raise AuthenticationFailed(
            #     "Key missing try to login" \
            #         " again (you logged out by timeout)"
            # )
        try:
            if not access_token:
                # user = AnonymousUser()
                raise AuthenticationFailed(
                    'unaunticated access token missing'
                )
            try:
                payload = jwt.decode(
                    access_token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                    )
                user = User.objects.get(id=payload['user_id'])
            except jwt.ExpiredSignatureError:
                # raise AuthenticationFailed(
                #     'unautneticated'
                # )
                user = AnonymousUser()
            except jwt.InvalidSignatureError:
                user = AnonymousUser()
        except UnboundLocalError:
            user = AnonymousUser()
        
        return user
