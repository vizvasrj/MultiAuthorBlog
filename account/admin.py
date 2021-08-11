from django.contrib import admin

from .models import Profile,Contact
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
    

admin.site.register(Contact)