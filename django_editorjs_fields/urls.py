from django.urls import path

from .views import ImageUploadView

urlpatterns = [
    path(
        'image_upload/', ImageUploadView.as_view(),
        name='editorjs_image_upload',
    ),
]
