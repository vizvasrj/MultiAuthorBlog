from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "es" in settings.ADMIN_SWITCH:
    from .models import SpanishTranslatedPost
    admin.site.register(SpanishTranslatedPost)
