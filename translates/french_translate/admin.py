from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "fr" in settings.ADMIN_SWITCH:
    from .models import FrenchTranslatedPost
    admin.site.register(FrenchTranslatedPost)
