from django.contrib import admin
from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "nn" in settings.ADMIN_SWITCH:
    from .models import NorwegianTranslatedPost, NorwegianTranslatedTag
    admin.site.register(NorwegianTranslatedPost)
    admin.site.register(NorwegianTranslatedTag)
