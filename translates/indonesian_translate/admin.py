from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "id" in settings.ADMIN_SWITCH:
    from .models import IndonesianTranslatedPost, IndonesianTranslatedTag
    admin.site.register(IndonesianTranslatedPost)
    admin.site.register(IndonesianTranslatedTag)
