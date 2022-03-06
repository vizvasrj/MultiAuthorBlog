from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "zh-hans" in settings.ADMIN_SWITCH:
    from .models import ChineseTranslatedPost, ChineseTranslatedTag
    admin.site.register(ChineseTranslatedPost)
    admin.site.register(ChineseTranslatedTag)
