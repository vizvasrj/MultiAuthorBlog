from django.contrib import admin
from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "ar" in settings.ADMIN_SWITCH:
    from .models import ArabicTranslatedPost, ArabicTranslatedTag
    admin.site.register(ArabicTranslatedPost)
    admin.site.register(ArabicTranslatedTag)
