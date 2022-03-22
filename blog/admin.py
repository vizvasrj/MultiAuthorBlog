from curses.ascii import SO
from django.contrib import admin
from .models import (
    Post, Comment, Image,
    Occurrence, Sources, TagPostOccurrenceLen    
)

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('-publish',)


@admin.register(Comment)
class CommedntAdmin(admin.ModelAdmin):
    ordering = ('-created',)

# 

admin.site.register(Image)
admin.site.register(Occurrence)
admin.site.register(TagPostOccurrenceLen)
admin.site.register(Sources)
