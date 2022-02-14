from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


# local
from . import views , rest_views
from .forms import (
    UserPasswordResetForm, UserPasswordChangeForm
)

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
     # path('',
     #      TemplateView.as_view(template_name="account_base.html")),
     path('login/',
          views.user_login, name='login'),

     #     path('login/',
     #          auth_views.LoginView.as_view(), name='login'),
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

     path('my/published/', views.my_published_stories, name='my_published_story'),
     path('my/drafted/', views.my_drafted_stories, name='my_drafted_story'),
     path('my/trashed/', views.my_trashed_stories, name='my_trashed_story'),

     path('my/published/trash/', views.trash_post, name='trash_published_post'),
     path('my/drafted/trash/', views.trash_post, name='trash_drafted_post'),
     path('my/trashed/delete/', views.delete_post, name='delete_trashed_post'),

     path('my/drafted/publish/', views.publish_post, name='publish_drafted_post'),
     path('my/trashed/untrash/', views.untrash_post, name='untrash_trashed_post'),

     path('account/delete/', views.delete_profile, name='delete_profile'),

     path('they/shared/', views.shared_post_by_other, name='their_shared_post'),
     path('they/shared/remove_me/', views.remove_shared_post_by_other, name='remove_there_shared_post'),

     path('my/shared/', views.shared_post_by_me, name='my_shared_post'),
     path('my/shared/remove_me/', views.remove_shared_post_by_me, name='remove_my_shared_post'),


     # Validates
     path('account/validate_username', views.validate_username, name='validate_username'),
     path('account/validate_email', views.validate_email, name='validate_email'),

     path('', views.my_relations_posts, name='my_relations_posts'),


     # Rest framwork authentication
     path('api/logout/', rest_views.LogoutView.as_view(), 
          name='api-logout'),
     path('api/token/', rest_views.MyTokenObtainPairView.as_view(),
          name='token_create'),
     path('api/token/refresh/',
          jwt_views.TokenRefreshSlidingView.as_view(),
          name='refresh'),
     path('api/register/',
          rest_views.AuthUserRegistrationView.as_view(),
          name='api-register'),
     path('api/login/',
          rest_views.AuthUserLoginView.as_view(),
          name='api-login'),
     path('api/users/',
          rest_views.UserListView.as_view(),
          name='api-users'),

     path('api/loginchecker/', rest_views.LoginCheckerView.as_view(), name='login_checker'),


]
