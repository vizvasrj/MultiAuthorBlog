from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "de" in settings.ADMIN_SWITCH:
    from .models import GermanTranslatedPost, GermanTranslatedTag
    admin.site.register(GermanTranslatedPost)
    admin.site.register(GermanTranslatedTag)
