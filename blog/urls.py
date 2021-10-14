from django.urls import path
from django.views.generic import TemplateView

from .views import (
    create_post, post_detail, post_list, post_search,
    post_like, comment_like, bookmark, update_data,
    delete_post, edit_comment, tag_list
)

from . import views



urlpatterns = [
    path('create/', create_post, name='post_new'),
    path('list/', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, 
        name='post_list_by_tag'),
    path('post/search/', post_search, name='post_search'),
    path('post/like/', post_like, name='like'),
    path('comment/like/', comment_like, name='comment_like'),
    path('post/bookmark/', bookmark, name='bookmark'),
    path('update/<int:pk>/', update_data, name='edit_post'),
    path('delete/<int:pk>/', delete_post,
        name='delete_post'),
    path('404/', TemplateView.as_view(
        template_name='blog/utility/404.html'
    ), name='404'),
    path('update_comment/<int:pk>/', edit_comment,
        name='edit_comment'),
    path('tags/list/', tag_list, name='tag_list'),
    path('post/search-ajax/', views.post_ajax_search, name='search_ajax'),


]