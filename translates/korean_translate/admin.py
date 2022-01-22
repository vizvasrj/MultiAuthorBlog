from django.contrib import admin

from django.conf import settings

from MultiAuthorBlog.settings import ADMIN_SWITCH
if "ko" in settings.ADMIN_SWITCH:
    from .models import KoreanTranslatedPost
    admin.site.register(KoreanTranslatedPost)
