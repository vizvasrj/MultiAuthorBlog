# Django
from django.db import models
import time
from django.forms.widgets import Textarea
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# local
from account.models import Profile

# 3rd party
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey


now = timezone.now()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(
            PublishedManager, self
        ).get_queryset().filter(
            publish__lte=now
            # status='published'
        )
    

class DraftedManager(models.Manager):
    def get_queryset(self):
        return super(
            DraftedManager, self
        ).get_queryset().filter(
            status='draft'
        )

def custome_slugify(value):
    # change url like 
    # slug=title-1628829161_1792307
    t = str(time.time()).replace('.','_')
    return f'{value}-{t}'

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from='title',
        slugify=custome_slugify,
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    cover = models.ImageField(
        upload_to='category/',
        default='category/defaultcatg.jpg',
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cover = models.ImageField(
        upload_to='cover/%Y/%m/%d',
        blank=True, null=True
    )
    slug = AutoSlugField(
        populate_from='title',
        # slugify=custome_slugify,
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )
    objects = models.Manager()
    published = PublishedManager()
    drafted = DraftedManager()
    tags = TaggableManager()
    users_like = models.ManyToManyField(
        User,
        related_name='posts_liked',
        blank=True
    )
    bookmark_list = models.ManyToManyField(
        User,
        related_name='post_bookmark',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'post_detail',
            args = [self.slug]
        )

class Comment(MPTTModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    commentor = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_comments'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    users_like = models.ManyToManyField(
        User,
        related_name='comments_liked',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )

    class MPTTMeta:
        order_instertion_by = ['-publish']

    def __str__(self):
        return f'comment by {self.commentor} on {self.post__title}'