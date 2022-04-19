from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "bn" in settings.ADMIN_SWITCH:
    from .models import BengaliTranslatedPost, BengaliTranslatedTag
    admin.site.register(BengaliTranslatedPost)
    admin.site.register(BengaliTranslatedTag)
