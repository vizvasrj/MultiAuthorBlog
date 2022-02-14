from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from django.conf import settings

import jwt
from django.contrib.auth.models import User
from .serializers import (
    LoginCheckerSerializer, UserListSerializer, UserRegistrationSerializer,
    UserLoginSerializer, MyTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from django.http import JsonResponse, response
from termcolor import colored
from rest_framework.settings import api_settings
from rest_framework import permissions

from account.models import Profile

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return JsonResponse(routes)


class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        print(colored(request.user, 'red'))

        if valid:
            serializer.save()
            data = serializer.data
            try:
                data.pop('password')
            except KeyError:
                pass
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': data
            }
            return Response(response, status=status_code)

class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'login sucessfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                }
            }
            r = Response(response)
            r.set_cookie(key='jwtt', value=serializer.data['access'])

            return r

def auth(request):
    try:
        bearer = request.headers
        try:
            s = bearer['Authorization']
            access_token = s.split(' ')[1]
        except KeyError:
            access_token = request.COOKIES['jwtt']
    except KeyError:
        raise AuthenticationFailed(
            "Key missing try to login" \
                " again (you logged out by timeout)"
        )
    if not access_token:
        raise AuthenticationFailed(
            'unaunticated access token missing'
        )
    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=['HS256']
            )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed(
            'unautneticated'
        )
    user = User.objects.get(id=payload['user_id'])
    return user


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    
    def get(self, request):
        user = auth(request=request)
        if user:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Successfully fetched users',
                'users': serializer.data
            }
            
    
            return Response(
                response, status=status_code
            )  
    
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                'success': False,
                'status_code': status_code,
                'message': 'UserDoes not authorized'
            }
            return Response(response, status=status_code)

class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwtt')
        response.data = {
            'message': 'logout successfully'
        }
        return response


class LoginCheckerView(generics.ListAPIView):
    # queryset = Profile.objects.all()
    serializer_class = LoginCheckerSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    def get(self, request):
        user = auth(request=request)
        if user:
            users = Profile.objects.get(user__username=request.user.username)
            serializer = self.serializer_class(users)
            
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': 'Successfully fetched users',
                'users': serializer.data
            }
            
    
            return Response(
                response, status=status_code
            )  
    
        else:
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                'success': False,
                'status_code': status_code,
                'message': 'UserDoes not authorized'
            }
            return Response(response, status=status_code)
