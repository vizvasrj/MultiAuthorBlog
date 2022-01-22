from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "ru" in settings.ADMIN_SWITCH:
    from .models import RussianTranslatedPost
    admin.site.register(RussianTranslatedPost)
