from tokenize import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import User
from django.http import request

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Profile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, write_only=True,
        style = {
            'input_type': 'password',
            'placeholder': 'Password'
        }, required=True
    )
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )
    def create(self, validated_data):
        auth_user = User.objects.create_user(
            **validated_data
        )
        return auth_user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=128
    )
    password = serializers.CharField(
        max_length=128, write_only=True
    )
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'invalid login credential'
            )
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(
                None, user
            )
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exesists')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email',
        )

class LoginCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'user',
            'full_name',
        )