from django.contrib import admin
from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "nn" in settings.ADMIN_SWITCH:
    from .models import NorwegianTranslatedPost
    admin.site.register(NorwegianTranslatedPost)
