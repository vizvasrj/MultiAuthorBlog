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

class ChineseTranslatedTag(models.Model):
    tag = models.ForeignKey(
        MyCustomTag,
        related_name='chinese_tags',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = ['id']





class ChineseTranslatedPost(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='chinese_translated_post',
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
        related_name='chinese_translate_edited_by'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(
        User,
        related_name='chinese_translated_users_like',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )
    bookmark_list = models.ManyToManyField(
        User,
        related_name='chinese_translated_bookmark',
        blank=True
    )
    audio = models.FileField(
        upload_to='chinese_speech/',
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
            'chinese_post_detail',
            args = [self.slug]
        )

from about.models import AboutPost

class ChineseTranslatedAbout(models.Model):
    post = models.ForeignKey(
        AboutPost,
        related_name='chinese_about',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=256)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated']
        get_latest_by = ['created']
