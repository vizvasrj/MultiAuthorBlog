from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "vi" in settings.ADMIN_SWITCH:
    from .models import VietnameseTranslatedPost
    admin.site.register(VietnameseTranslatedPost)
