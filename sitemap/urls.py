from django.urls import path
from .views import sitemap_list, sitemap_detail
urlpatterns = [
    path('sitemap.xml', sitemap_list, name='sitemap_list'),
    path('sitemap/<str:name>', sitemap_detail, name='sitemap_detail'),
]