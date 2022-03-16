from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from django.contrib.auth.models import AnonymousUser, User
from rest_framework import authentication, permissions
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
from rest_framework.response import Response
from django.db.models import Q
from .serializers import HLPSerializer, UntranslatedSerializer
from scrape.models import Healthline, HealthlineParsed
from django_filters.rest_framework import DjangoFilterBackend
from account.models import Profile
from rest_framework import status
from django.conf import settings
import redis
import jwt
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


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

# Create your views here.
class HPPostView(ListCreateAPIView):
    queryset = HealthlineParsed.objects.all()
    serializer_class = HLPSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['url', ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class UntranslatedView(ListCreateAPIView):
#     queryset = Healthline.objects.all()
#     serializer_class = UntranslatedSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['url', ]

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


class UntranslatedView(ListCreateAPIView):
    query = Healthline.objects.all()
    
    queryset = query
    serializer_class = UntranslatedSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['url', ]

    def list(self, request, *args, **kwargs):
        if request.user != AnonymousUser():
            pass
        else:
            raise AuthenticationFailed(
                reverse(
                    'api-login',
                    request=request
                )            
            )
        queryset = Healthline.objects.all().filter(
        ).order_by("?")[0:1]

        p = queryset[0]
        # p = Healthline.objects.all().order_by("-created")[0]
        rp = r.smembers("usedone5")
        # print(rp)
        stringlist = [x.decode("utf-8") for x in rp]
        # print(stringlist)
        set_list = set(stringlist)
        # print(set_list)
        p = Healthline.objects.filter(
            # cover2=None
            ).order_by(
                "id"
            ).filter(
                ~Q(id__in=set_list)
            )[0]
        # print(p)
        r.sadd("usedone5", p.id)
        queryset = Healthline.objects.all().filter(id=p.id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # user = get_user(request)
        # if user.is_authenticated:
        #     return user
        user = auth(request=request)
        if user:
            return self.create(request)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()
