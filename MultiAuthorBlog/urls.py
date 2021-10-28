import debug_toolbar
from os import name
from blog.models import Post
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import read_file
from blog.views import post_detail, tags_posts_lists
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
urlpatterns = i18n_patterns(
    path('__debug__/', include(debug_toolbar.urls)),

    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    # path('', post_list),
    path('blog/', include('blog.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('my_uploader/', include('image_uploader.urls')),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('select2/', include('django_select2.urls')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('about/', include('about.urls')),
    path('.well-known/pki-validation/', read_file),
    path('publication/', include('publication.urls')),
    path('<str:author>/<slug:slug>/',
         post_detail, name='post_detail'),
    path('tag/<slug:slug>', tags_posts_lists, 
            name='tags_posts_lists'),

)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
