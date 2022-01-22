from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "en" in settings.ADMIN_SWITCH:
    from .models import EnglishTranslatedPost
    admin.site.register(EnglishTranslatedPost)
