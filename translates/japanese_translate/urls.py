from django.urls import path
from .views import JTPostDetail, JTPostView

urlpatterns = [
    path('tr/post/', JTPostView.as_view(), name='ja_list'),
    path('tr/post/<int:pk>/', JTPostDetail.as_view(), name='ja_detail')
]