from django.contrib import admin

# Register your models here.
from .models import AboutPost, AboutPostTranslated
from parler.admin import TranslatableAdmin

admin.site.register(AboutPost)


# admin.site.register(TranslatedAbout)

@admin.register(AboutPostTranslated)
class ProductAdmin(TranslatableAdmin):
    list_display = ['title', 'slug']
    list_filter = ['created', 'updated']
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}

