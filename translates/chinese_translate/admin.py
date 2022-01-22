from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "zh-hans" in settings.ADMIN_SWITCH:
    from .models import ChineseTranslatedPost
    admin.site.register(ChineseTranslatedPost)
