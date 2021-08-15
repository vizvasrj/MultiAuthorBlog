from django.urls import path

from .views import (
    create_post, post_detail, post_list
)

urlpatterns = [
    path('create/', create_post, name='post_new'),
    path('list/', post_list, name='post_list'),
    path('<slug:post>/',
         post_detail, name='post_detail'),
]
