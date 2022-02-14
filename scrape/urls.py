from .views import HPPostView
from django.urls import path

urlpatterns = [
    path('hp/post/', HPPostView.as_view(), name='hp_list'),
]