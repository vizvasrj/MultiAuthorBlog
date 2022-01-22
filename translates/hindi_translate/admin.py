from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "hi" in settings.ADMIN_SWITCH:
    from .models import HindiTranslatedPost
    admin.site.register(HindiTranslatedPost)
