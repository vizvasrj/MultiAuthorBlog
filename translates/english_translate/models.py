from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.urls import reverse
from django.utils.text import slugify

from taggit_autosuggest.managers import TaggableManager
from autoslug import AutoSlugField
from unidecode import unidecode

# Create your models here.
from blog.models import Post
from mytag.models import MyCustomTag

class EnglishTranslatedTag(models.Model):
    tag = models.ForeignKey(
        MyCustomTag,
        related_name='english_tags',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = ['id']





class EnglishTranslatedPost(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='english_translated_post',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=256
    )
    slug = AutoSlugField(
        populate_from='title',
    )
    body = models.TextField()
    meta_description = models.CharField(max_length=160, null=True, blank=True)
    tags = TaggableManager()
    cover = models.ImageField(
        upload_to='cover/%Y/%m/%d',
        blank=True, null=True
    )
    edited_by = models.ManyToManyField(
        User,
        related_name='english_translate_edited_by'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(
        User,
        related_name='english_translated_users_like',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )
    bookmark_list = models.ManyToManyField(
        User,
        related_name='english_translated_bookmark',
        blank=True
    )
    audio = models.FileField(
        upload_to='english_speech/',
        blank=True
    )
    translate = models.BooleanField(
        default=True
    )
    audio_url = models.URLField(
        blank=True,
        null=True
    )
    g_audio_url = models.URLField(
        blank=True,
        null=True
    )
    class Meta:
        ordering = ['-updated']
        get_latest_by = ['created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'english_post_detail',
            args = [self.slug]
        )

