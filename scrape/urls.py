from .views import HPPostView, UntranslatedView
from django.urls import path

urlpatterns = [
    path('hp/post/', HPPostView.as_view(), name='hp_list'),
    path('untranslated/post/', UntranslatedView.as_view(), name='untranslated_list'),
]