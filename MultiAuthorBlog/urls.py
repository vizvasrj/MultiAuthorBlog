from blog.models import Post
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('blog/', include('blog.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('select2/', include('django_select2.urls')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('about/', include('about.urls')),


]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
