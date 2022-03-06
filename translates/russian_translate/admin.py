from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "ru" in settings.ADMIN_SWITCH:
    from .models import RussianTranslatedPost, RussianTranslatedTag
    admin.site.register(RussianTranslatedPost)
    admin.site.register(RussianTranslatedTag)
