from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "ja" in settings.ADMIN_SWITCH:
    from .models import JapaneseTranslatedPost
    admin.site.register(JapaneseTranslatedPost)
