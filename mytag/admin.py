from django.contrib import admin

# Register your models here.
from mytag.models import MyCustomTag
from mytag.models import TagNameValue, TagContact
admin.site.register(TagNameValue)
admin.site.register(TagContact)

admin.site.register(MyCustomTag)