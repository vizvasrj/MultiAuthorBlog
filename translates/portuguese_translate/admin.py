from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "pt" in settings.ADMIN_SWITCH:
    from .models import PortugueseTranslatedPost, PortugueseTranslatedTag
    admin.site.register(PortugueseTranslatedPost)
    admin.site.register(PortugueseTranslatedTag)
