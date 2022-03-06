from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "vi" in settings.ADMIN_SWITCH:
    from .models import VietnameseTranslatedPost, VietnameseTranslatedTag
    admin.site.register(VietnameseTranslatedPost)
    admin.site.register(VietnameseTranslatedTag)
