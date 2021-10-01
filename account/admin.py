from django.contrib import admin

from .models import Profile,Contact, Theme
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'user_id']
    

admin.site.register(Contact)
admin.site.register(Theme)