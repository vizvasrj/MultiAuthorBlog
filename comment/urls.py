from django.urls import path

from .views import c_comment_like, edit_comment


urlpatterns = [
    path('like/', c_comment_like, name='c_comment_like'),
    path('edit/<int:pk>/<int:aid>/', edit_comment, name='edit_comment2'),

]