from django.contrib import admin
from taggit.models import Tag
from .models import Post, Comment, MyCustomTag

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommedntAdmin(admin.ModelAdmin):
    ordering = ('-created',)

# 
admin.site.register(MyCustomTag)

from .models import TagNameValue, TagContact
admin.site.register(TagNameValue)
admin.site.register(TagContact)
