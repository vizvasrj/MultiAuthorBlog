from django.forms import ValidationError
from .models import Post, Image, Occurrence
from account.models import Profile

from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from rest_framework.reverse import reverse 

from .serializers import OnlyAudioShow, PostCURDSerializer, PostSerializer, SourcePostSerializer
from rest_framework.exceptions import (
    AuthenticationFailed, PermissionDenied, ValidationError,
    
    
)
from rest_framework.exceptions import APIException
import jwt
from rest_framework import status
from django.contrib.auth.middleware import get_user
from .permissions import IsOwnerOrReadOnly
from termcolor import colored
from django.contrib.auth.models import AnonymousUser

from mytag.models import MyCustomTag
import io
import os
import base64
from django.core.files import File
import json


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
            im_b64 = request.data['cover2.image']
            cover2_name = request.data['cover2._name']
            creator_name = request.data['cover2.creator_name']
            creator_url = request.data['cover2.creator_url']
            tags = request.data['post.tags']
            # audio_urls = request.data['audio_url']
            # print(colored(audio_urls, 'green'), 'auio_url')
            # qq = json.loads(audio_urls)
            # print(colored(qq, 'red'))
            # for x in qq:
            #     print(x)
            #     l_key = list(x.keys())[0]
            #     print(l_key)
            #     l_url = list(x.values())[0]
            #     print(l_url)

            #     if l_key == 'ja':
            #         i_tr = instance.japanese_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'en':
            #         i_tr = instance.english_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'ar':
            #         i_tr = instance.arabic_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'zh_CN':
            #         i_tr = instance.chinese_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'tl':
            #         i_tr = instance.filipino_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'fr':
            #         i_tr = instance.french_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'de':
            #         i_tr = instance.german_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'hi':
            #         i_tr = instance.hindi_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'id':
            #         i_tr = instance.indonesian_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'it':
            #         i_tr = instance.italian_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'ko':
            #         i_tr = instance.korean_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'no':
            #         i_tr = instance.norwegian_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'pt':
            #         i_tr = instance.portuguese_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'ru':
            #         i_tr = instance.russian_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
            #     elif l_key == 'es':
            #         i_tr = instance.spanish_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
                
            #     elif l_key == 'vi':
            #         i_tr = instance.vietnamese_translated_post.latest()
            #         i_tr.audio_url = l_url
            #         i_tr.save()
                


            # 999999999999999999999999999999999999
            tag_json_loads = json.loads(tags)
            # 
            for idx, x in enumerate(tag_json_loads):
                tag_name = x["tag"]
                tag_occurrence = x["occurrence"]
                ar = x["ar"]
                hi = x["hi"]
                zh_CN = x["zh_CN"]
                ta = x["ta"]
                fr = x["fr"]
                de = x["de"]
                id = x["id"]
                it = x["it"]
                ja = x["ja"]
                ko = x["ko"]
                no = x["no"]
                pt = x["pt"]
                ru = x["ru"]
                es = x["es"]
                vi = x["vi"]
                en = x["en"]
                try:
                    tag = MyCustomTag.objects.get_or_create(name=tag_name)[0]
                    occurrence = Occurrence.objects.get_or_create(number=tag_occurrence)[0]
                    instance.tag_occurence.get_or_create(
                        tag=tag,
                        tag_count=occurrence,
                    )
                    instance.tags.add(tag_name)
                    tag.arabic_tags.get_or_create(tag=tag, name=ar)[0]
                    tag.hindi_tags.get_or_create(tag=tag, name=hi)[0]
                    tag.chinese_tags.get_or_create(tag=tag, name=zh_CN)[0]
                    tag.filipino_tags.get_or_create(tag=tag, name=ta)[0]
                    tag.french_tags.get_or_create(tag=tag, name=fr)[0]
                    tag.german_tags.get_or_create(tag=tag, name=de)[0]
                    tag.indonesian_tags.get_or_create(tag=tag, name=id)[0]
                    tag.italian_tags.get_or_create(tag=tag, name=it)[0]
                    tag.japanese_tags.get_or_create(tag=tag, name=ja)[0]
                    tag.korean_tags.get_or_create(tag=tag, name=ko)[0]
                    tag.norwegian_tags.get_or_create(tag=tag, name=no)[0]
                    tag.portuguese_tags.get_or_create(tag=tag, name=pt)[0]
                    tag.russian_tags.get_or_create(tag=tag, name=ru)[0]
                    tag.spanish_tags.get_or_create(tag=tag, name=es)[0]
                    tag.vietnamese_tags.get_or_create(tag=tag, name=vi)[0]
                    tag.english_tags.get_or_create(tag=tag, name=en)[0]
                except TypeError:
                    pass
            head = str(im_b64[:10])
            if head.startswith('iVBORw0KGg'):
                ext = 'png'
            elif head.startswith('/9j/'):
                ext = 'jpg'
            else:
                ext = 'jpg'

            try:
                cover2 = Image.objects.get(sha_256=cover2_name)
                # print(colored("cover2 sha exists", 'blue'))
            except Image.DoesNotExist:
                with open(f'{cover2_name}.{ext}', 'wb') as fh:
                    fh.write(base64.urlsafe_b64decode(im_b64))

                new_image = File(open(f'{cover2_name}.{ext}', 'rb'))
                cover2 = Image.objects.create(
                    image=new_image, 
                    creator_name=creator_name, 
                    creator_url=creator_url,
                    sha_256=cover2_name
                )
                # print(colored(os.popen('ls').read(), 'red'))
                try:
                    os.remove(f'{cover2_name}.{ext}')
                except FileNotFoundError:
                    pass
            

            data_ser = {
                "title": title, 
                "body": body, 
                "status": status, 
                "t": data_req,
                "cover2": cover2.id
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
            raise AuthenticationFailed(
                reverse(
                    'api-login',
                    request=request
                )            
            )
        queryset = Post.aupm.all().filter(
            cover2=None
        ).order_by("?")[0:1]

        p = queryset[0]
        # p = Post.objects.all().order_by("-created")[0]
        rp = r.smembers("usedone5")
        # print(rp)
        stringlist = [x.decode("utf-8") for x in rp]
        # print(stringlist)
        set_list = set(stringlist)
        # print(set_list)
        p = Post.objects.filter(
            # cover2=None
            ).order_by(
                "-created"
            ).filter(
                ~Q(id__in=set_list)
            )[0]
        # print(p)
        r.sadd("usedone5", p.id)
        queryset = Post.objects.all().filter(id=p.id)
        
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


"""Audio are here"""
# Custome execption
class Success(APIException):
    status_code = status.HTTP_202_ACCEPTED
    default_detail = 'Success .'
    default_code = 'success'


class AudioPostCRUDView(generics.ListCreateAPIView):
    query = Post.aupm.all()
    
    queryset = query
    serializer_class = OnlyAudioShow
    '''In this code i am using redis to store keys of post which 
    are used by worker to run api to translate and not returing that id again
    to some else worker that is i dont want to translate posts more than two
    times its bad for resource.'''

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
        queryset = Post.aupm.all().filter(
            cover2=None
        ).order_by("?")[0:1]

        p = queryset[0]
        # p = Post.objects.all().order_by("-created")[0]
        rp = r.smembers("new5")
        # print(rp)
        stringlist = [x.decode("utf-8") for x in rp]
        # print(stringlist)
        set_list = set(stringlist)
        # print(set_list)
        p = Post.objects.filter(
            # cover2=None
            ).order_by( # delete id 16274 later
                "-created"
            ).filter(
                ~Q(id__in=set_list)
            )[0]
        # print(p)
        r.sadd("new5", p.id)
        queryset = Post.objects.all().filter(id=p.id)
        
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


# class AudioPostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = OnlyAudioShow
#     name = 'audio-post-detail'
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         # IsOwnerOrReadOnly
#     )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         audio_urls = request.data['audio_url']
#         qq = json.loads(audio_urls)
        # for x in qq:
        #     l_key = list(x.keys())[0]
        #     print(l_key)
        #     l_url = list(x.values())[0]
            
        #     if l_key == 'ja':
        #         i_tr = instance.japanese_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'en':
        #         i_tr = instance.english_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'ar':
        #         i_tr = instance.arabic_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'zh_CN':
        #         i_tr = instance.chinese_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'tl':
        #         i_tr = instance.filipino_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'fr':
        #         i_tr = instance.french_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'de':
        #         i_tr = instance.german_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'hi':
        #         i_tr = instance.hindi_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'id':
        #         i_tr = instance.indonesian_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'it':
        #         i_tr = instance.italian_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'ko':
        #         i_tr = instance.korean_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'no':
        #         i_tr = instance.norwegian_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'pt':
        #         i_tr = instance.portuguese_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'ru':
        #         i_tr = instance.russian_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
        #     elif l_key == 'es':
        #         i_tr = instance.spanish_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()
            
        #     elif l_key == 'vi':
        #         i_tr = instance.vietnamese_translated_post.latest()
        #         i_tr.audio_url = None
        #         i_tr.audio_url = l_url
        #         i_tr.save()

        # raise Success("Success")

class AudioPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = OnlyAudioShow
    name = 'audio-post-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly
    )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        audio_urls = request.data['audio_url']
        qq = json.loads(audio_urls)

        for x in qq:
            if x['ln'] == 'ja':
                i_tr = instance.japanese_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'en':
                i_tr = instance.english_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'ar':
                i_tr = instance.arabic_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'zh_CN':
                i_tr = instance.chinese_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'tl':
                i_tr = instance.filipino_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'fr':
                i_tr = instance.french_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'de':
                i_tr = instance.german_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'hi':
                i_tr = instance.hindi_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'id':
                i_tr = instance.indonesian_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'it':
                i_tr = instance.italian_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'ko':
                i_tr = instance.korean_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'no':
                i_tr = instance.norwegian_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'pt':
                i_tr = instance.portuguese_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'ru':
                i_tr = instance.russian_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            elif x['ln'] == 'es':
                i_tr = instance.spanish_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()
            
            elif x['ln'] == 'vi':
                i_tr = instance.vietnamese_translated_post.latest()
                i_tr.g_audio_url = None
                i_tr.g_audio_url = x['url']
                i_tr.save()

        raise Success("Success")


# class SourcePostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = SourcePostSerializer
#     name = 'audio-post-detail'
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         # IsOwnerOrReadOnly
#     )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         audio_urls = request.data['sources']
#         qq = json.loads(audio_urls)
#         for


#         raise Success("Success")