from django.urls import path
from .views import FRTPostDetail, FRTPostView

urlpatterns = [
    path('tr/post/', FRTPostView.as_view(), name='it_list'),
    path('tr/post/<int:pk>/', FRTPostDetail.as_view(), name='it_detail')
]