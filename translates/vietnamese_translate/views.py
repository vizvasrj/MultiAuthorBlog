from django.conf import settings
from django.contrib.auth.models import User


from .serializers import FRTPostSerializer
from translates.vietnamese_translate.models import VietnameseTranslatedPost

from rest_framework import generics, status, permissions
from rest_framework.exceptions import (
    AuthenticationFailed, ValidationError, PermissionDenied
)
import jwt
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from termcolor import colored

from blog.models import Post

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
class FRTPostView(generics.ListCreateAPIView):
    queryset = VietnameseTranslatedPost.objects.all()
    serializer_class = FRTPostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
        user = User.objects.filter(username=user)
        data = serializer.validated_data
        post_id = data['post']['id']
        post = Post.aupm.get(id=post_id)
        serializer.save(post=post, edited_by=user)


class FRTPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VietnameseTranslatedPost.objects.all()
    serializer_class = FRTPostSerializer
    name = 'fr-post-list'
    permission_class = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def update(self, request, *args, **kwargs):
        # post = request.data['post']
        # if post.isdigit():
        #     pass
        # else:
        #     raise ValidationError(
        #         "post must be positive integer example 101"
        #         )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, instance):
        user = self.request.user
        user = User.objects.get(username=user)
        path_id = instance.id
        data = serializer.validated_data
        post_id = data['post']['id']
        p = VietnameseTranslatedPost.objects.get(id=path_id)
        p.edited_by.add(user)
        post = Post.objects.get(id=post_id)
        serializer.save(post=post)

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
        if user in instance.edited_by.all() and instance.edited_by.all().count() == 1:
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied(
                "You dont have permission to delete it"
            )
