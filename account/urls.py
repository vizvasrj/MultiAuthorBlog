from django.urls import path
from django.views.generic import TemplateView

# local
from . import views

urlpatterns = [
    path('',
        TemplateView.as_view(template_name="account_base.html")),
    path('login/',
        views.user_login, name='user_login'),
    path('register/',
        views.register, name='register'),


]
