from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


# local
from . import views
from .forms import (
    UserPasswordResetForm, UserPasswordChangeForm
)

urlpatterns = [
    path('',
         TemplateView.as_view(template_name="account_base.html")),
    # path('login/',
    #      views.user_login, name='user_login'),

    path('login/',
         auth_views.LoginView.as_view(), name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='registration/logout.html'
         ), name='logout'),

    # path('password_change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        form_class=UserPasswordChangeForm), name='password_change'),


    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Reset password urls
    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        form_class=UserPasswordResetForm), name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('register/',
         views.register, name='register'),

    path('edit/', views.edit, name='edit'),

    path('users/', views.user_list, name='user_list'),

    path('<str:username>/',
         views.user_detail, name='user_detail'),

    path('users/follow',
         views.user_follow, name='user_follow'),

    # path('my/profile/', views.me_page, name='me'),

    path('my/profile/', views.me, name='my_profile'),

    path('<str:username>/following/',
         views.user_following, name='user_following'),

    path('<str:username>/follower/',
         views.user_follower, name='user_follower'),

]
