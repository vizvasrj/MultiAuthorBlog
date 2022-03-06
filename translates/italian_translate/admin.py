from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "it" in settings.ADMIN_SWITCH:
    from .models import ItalianTranslatedPost, ItalianTranslatedTag
    admin.site.register(ItalianTranslatedPost)
    admin.site.register(ItalianTranslatedTag)
