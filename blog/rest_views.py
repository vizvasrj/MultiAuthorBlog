from django.forms import ValidationError
from .models import Post
from account.models import Profile

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from rest_framework.reverse import reverse 

from .serializers import PostCURDSerializer, PostSerializer
from rest_framework.exceptions import (
    AuthenticationFailed, PermissionDenied, ValidationError,
    NotFound
)
import jwt
from rest_framework import status
from django.contrib.auth.middleware import get_user
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from termcolor import colored
from django.contrib.auth.models import AnonymousUser

from blog import serializers



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

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class PostCRUDView(generics.ListCreateAPIView):
    queryset = Post.aupm.all()
    serializer_class = PostCURDSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # user = get_user(request)
        # if user.is_authenticated:
        #     return user
        user = auth(request=request)
        if user:
            return self.create(request, user=user.username)
        
    def create(self, request, user, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def perform_create(self, serializer, user):
        user = Profile.objects.get(user__username=user)
        serializer.save(author=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCURDSerializer
    name = 'post-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        t1 = instance.t
        try:
            t2 = request.data['t']
        except KeyError:
            raise ValidationError("Key Error try inputing 't'")
        author = request.user
        if str(request.user) != str(instance.author):
            author = instance.author
            try:
                if request.data['title'] != instance.title or request.data['body'] != instance.body or request.data['status'] != instance.status:
                    raise PermissionDenied("you dont have permissions")
            except KeyError:
                pass
        if t1 != t2:
            title = instance.title
            body = instance.body
            status = instance.status
            author = instance.author
            data_req = request.data['t']
            data_ser = {
                "title": title, 
                "body": body, 
                "status": status, 
                "t": data_req
                }
            json_d = data_ser
        elif t1 == t2:
            json_d = request.data
        elif t2 == []:
            json_d = request.data
        serializer = self.get_serializer(instance, data=json_d, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, author=author)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, author):
        user = author
        user = Profile.objects.get(user__username=user)
        serializer.save(author=user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        user = auth(request=request)
        if user:
            return self.update(request, *args, **kwargs)



    def patch(self, request, *args, **kwargs):
        user = auth(request=request)
        if user:
            return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = auth(request=request)
        instance = self.get_object()
        author = instance.author
        if str(user) == str(author):
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not authorized to delete it.")


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            # 'posts': reverse(
            #     PostList.name,
            #     request=request
            # ),
            'posts-list': reverse(
                'post-list-curd',
                request=request
            ),
            'logout': reverse(
                'api-logout',
                request=request
            ),
            'login': reverse(
                'api-login',
                request=request
            ),
            'register': reverse(
                'api-register',
                request=request
            ),
            'users': reverse(
                'api-users',
                request=request
            ),
            'posts2': reverse(
                'posts-list-2',
                request=request
            ),
            'ja_list': reverse(
                'ja_list',
                request=request
            ),
            'zh-hans_list': reverse(
                'zh-hans_list',
                request=request
            ),
            'ru_list': reverse(
                'ru_list',
                request=request
            ),
            'en_list': reverse(
                'en_list',
                request=request
            ),
            'ar_list': reverse(
                'ar_list',
                request=request
            ),
            'ta_list': reverse(
                'ta_list',
                request=request
            ),
            'fr_list': reverse(
                'fr_list',
                request=request
            ),
            'de_list': reverse(
                'de_list',
                request=request
            ),
            'hi_list': reverse(
                'hi_list',
                request=request
            ),
            'id_list': reverse(
                'id_list',
                request=request
            ),
            'it_list': reverse(
                'it_list',
                request=request
            ),
            'ko_list': reverse(
                'ko_list',
                request=request
            ),
            'nn_list': reverse(
                'nn_list',
                request=request
            ),
            'pt_list': reverse(
                'pt_list',
                request=request
            ),
            'es_list': reverse(
                'es_list',
                request=request
            ),
            'vi_list': reverse(
                'vi_list',
                request=request
            ),
        })


class PostListView(APIView):
    # queryset = Post.aupm.all()
    serializer_class = PostSerializer
    name = 'post-list-view'

    def get(self, request):
        user = auth(request=request)
        user_str = str(user.username)
        if user:
            posts = Post.aupm.all()
            serializer = self.serializer_class(posts, many=True)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status_code': status_code,
                'message': user_str+" Logged in",
                'posts': serializer.data
            }
            return Response(
                response, status=status_code
            )

    def post(self, request):

        user = auth(request=request)
        serializer = PostSerializer(data=request.data)
        # valid = serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'login successfully',
                'title': serializer.data['title'],
                'author': user.username,
                
            }
            return Response(
                response, status=status_code
            )
        # print(colored(user, 'red'))

        serializer.save(author=user)

import redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


# New Methods for randome get all non translated but only one at a time
class RandomPostCRUDView(generics.ListCreateAPIView):
    query = Post.aupm.all()
    
    queryset = query
    serializer_class = PostCURDSerializer
    '''In this code i am using redis to store keys of post which 
    are used by worker to run api to translate and not returing that id again
    to some else worker that is i dont want to translate posts more than two
    times its bad for resource.'''

    def list(self, request, *args, **kwargs):
        if request.user != AnonymousUser():
            pass
        else:
            raise AuthenticationFailed("Login again")
        # queryset = Post.aupm.all().filter(
        #     Q(indonesian_translated_post=None)
        #     & Q(portuguese_translated_post=None)
        #     & Q(vietnamese_translated_post=None)
        #     & Q(russian_translated_post=None)
        #     & Q(spanish_translated_post=None)
        #     & Q(norwegian_translated_post=None)
        #     & Q(korean_translated_post=None)
        #     & Q(japanese_translated_post=None)
        #     & Q(italian_translated_post=None)
        #     & Q(hindi_translated_post=None)
        #     & Q(german_translated_post=None)
        #     & Q(french_translated_post=None)
        #     & Q(filipino_translated_post=None)
        #     & Q(english_translated_post=None)
        #     & Q(chinese_translated_post=None)
        #     & Q(arabic_translated_post=None)
        # ).filter(other_author=None).order_by("?")[0:1]

        # p = queryset[0]
        # # p = Post.objects.all().order_by("-created")[0]
        # rp = r.lrange("tpostt2", 0, -1)
        # # print(rp)
        # stringlist = [x.decode("utf-8") for x in rp]
        # # print(stringlist)
        # set_list = set(stringlist)
        # # print(set_list)
        # p = Post.objects.all().order_by("?").filter(~Q(id__in=set_list))[0]
        # # print(p)
        # r.rpush("tpostt2", p.id)
        # queryset = Post.objects.all().filter(id=p.id)
        
        # # This will check that post ie p is empty after filtering ids
        # # if it empty then  
        # if not p:
        #     print(p)
        id_tt = r.lrange("we3", 0, -1)
        if not id_tt:

            ids = []
            for x in Post.aupm.all().filter(Q(indonesian_translated_post=None)):
                ids.append(x.id)
                # print("insde for id")
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(portuguese_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(vietnamese_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(russian_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(spanish_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(norwegian_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(korean_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(japanese_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(italian_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(hindi_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(german_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(french_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(filipino_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(english_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(chinese_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            for x in Post.aupm.all().filter(Q(arabic_translated_post=None)):
                ids.append(x.id)
                r.rpush("we3", x.id)
            id_tt = r.lrange("we3", 0, -1)

        stringlist2 = [x.decode("utf-8") for x in id_tt]
        set_list2 = set(stringlist2)

        p = Post.objects.all().order_by("?").filter(~Q(id__in=set_list2))[0]
        queryset = Post.objects.all().filter(id=p.id)
        # print(queryset)
        page = self.paginate_queryset(queryset)
        # try:
        #     q = queryset[0]
        # except IndexError:
        #     raise NotFound("not found i thinks its ended")
        # q.other_author.add(request.user)
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
            return self.create(request, user=user.username)
        
    def create(self, request, user, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def perform_create(self, serializer, user):
        user = Profile.objects.get(user__username=user)
        serializer.save(author=user)

