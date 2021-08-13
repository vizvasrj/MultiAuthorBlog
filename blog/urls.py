from django.urls import path

from .views import (
    create_post, post_list
)

urlpatterns = [
    path('post/new', create_post, name='post_new'),
    path('', post_list, name='post_list'),
]