import debug_toolbar
from os import name
from blog.models import Post
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import read_file
from blog.views import post_detail, tags_posts_lists
from blog.rest_views import ApiRoot
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
# from blog.sitemaps import PostSitemap

# from django.contrib.sitemaps.views import sitemap

# sitemaps = {
#     'posts': PostSitemap,
# }

urlpatterns = i18n_patterns(
    path('__debug__/', include(debug_toolbar.urls)),

    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    # path('', post_list),
    path('blog/', include('blog.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
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
    path('grappelli/', include('grappelli.urls')),
    path('ja/', include('translates.japanese_translate.urls')),
    path('fr/', include('translates.french_translate.urls')),
    path('ar/', include('translates.arabic_translate.urls')),
    path('hi/', include('translates.hindi_translate.urls')),
    path('zh-hans/', include('translates.chinese_translate.urls')),
    path('es/', include('translates.spanish_translate.urls')),
    path('id/', include('translates.indonesian_translate.urls')),
    path('pt/', include('translates.portuguese_translate.urls')),
    path('ru/', include('translates.russian_translate.urls')),
    path('de/', include('translates.german_translate.urls')),
    path('ko/', include('translates.korean_translate.urls')),
    path('nn/', include('translates.norwegian_translate.urls')),
    path('vi/', include('translates.vietnamese_translate.urls')),
    path('tl/', include('translates.filipino_translate.urls')),
    path('it/', include('translates.italian_translate.urls')),
    path('en/', include('translates.english_translate.urls')),
    path('scrape/', include('scrape.urls')),
)
urlpatterns += [
    path('my_uploader/', include('image_uploader.urls')),
    path('api/', ApiRoot.as_view(), name='api-root'),
    # path(
    #     'sitemap.xml',
    #     sitemap, {
    #         'sitemaps': sitemaps
    #         }, name='django.contrib.sitemaps.views.sitemap'
    # ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
