from django.urls import path
from . import views


urlpatterns = [
    path('post/',
        views.about_post_list_view,
        name='about_post_list_view'
    ),
    path('post/<str:slug>',
        views.about_post_detail,
        name='about_post_detail'
    ),
]
