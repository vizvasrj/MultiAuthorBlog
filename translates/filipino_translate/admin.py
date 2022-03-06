from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "ta" in settings.ADMIN_SWITCH:
    from .models import FilipinoTranslatedPost, FilipinoTranslatedTag
    admin.site.register(FilipinoTranslatedPost)
    admin.site.register(FilipinoTranslatedTag)
