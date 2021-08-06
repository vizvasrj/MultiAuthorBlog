from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


# local
from . import views

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
    path('register/',
         views.register, name='register'),
    path('edit/', views.edit, name='edit'),




]
