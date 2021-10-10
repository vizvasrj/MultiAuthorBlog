# Django
from django.db import models
import time
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.core.signals import request_finished
from django.core.validators import FileExtensionValidator


# local
from account.models import Profile
from publication.models import Publication as Pub
# 3rd party
from autoslug import AutoSlugField
# from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from taggit_autosuggest.managers import TaggableManager
# language detector for slug ie en, hi, de, fr etc
# 
# for slug to change it name for diffrent 
# language i am using unidecode
from unidecode import unidecode


now = timezone.now()


class ActiveUserPublishedManager(models.Manager):
    def get_queryset(self):
        return super(ActiveUserPublishedManager, self).get_queryset().filter(
            author__user__is_active=True
        ).filter(publish__lte=timezone.now()).filter(
            status='published'
        )



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(
            PublishedManager, self
        ).get_queryset().filter(
            # publish__lte=now
            status='published'
        )

class TrashedManager(models.Manager):
    def get_queryset(self):
        return super(
            TrashedManager, self
        ).get_queryset().filter(
            # publish__lte=now
            status='trashed'
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
        populate_from=['title','created'],
        # slugify=custome_slugify,
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
        ('trashed', 'Trashed'),
    )
    STATUS_CREATE = (
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
    publication = models.ForeignKey(
        Pub,
        on_delete=models.CASCADE,
        related_name='posts',
        blank=True,
        null=True
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
    other_author = models.ManyToManyField(
        User,
        related_name='other_authors',
        blank=True
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
    aupm = ActiveUserPublishedManager()
    drafted = DraftedManager()
    trashed = TrashedManager()
    tags = TaggableManager(blank=True)
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
    last_editeduser = models.ForeignKey(
        User,
        related_name='last_edited',
        on_delete=models.PROTECT,
        blank=True,
        null=True
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

# pre_save #




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
        order_instertion_by = ['publish']

    def __str__(self):
        return f'comment by {self.commentor} on {self.post}'


    

# @receiver(post_save, sender=Post)
# def post_save_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("Send email to ", instance.author)
#         instance.save()
#     else:
#         print(instance.title, " was just saved")


# This is to send email when author add post
# ie create post and add author to it 
# it send email to added author
@receiver(m2m_changed, sender=Post.other_author.through)
def user_liked_changed(reverse, instance, action, pk_set, model, *args, **kwargs):
    if action == 'post_add':
        print(action)
        for x in instance.other_author.all():
            subject = f"{instance.author.full_name} make you " \
                f"co-editor in his/her post {instance.title}."
            message = f"you can go to 127.0.0.1:8000/blog/update/{instance.id}/ or "\
                f" <a href='127.0.0.1:8000/blog/update/{instance.id}/'>Click here</a>" \
                    f" 127.0.0.1:8000/blog/{instance.slug}/ at  {instance}"
            send_mail(
                subject, message, 'root@vizvasrj.com', (x.email,), fail_silently=False
            )
            



# @receiver(m2m_changed, sender=Post.other_author.through)
# def user_add(sender, reverse, instance, action, pk_set, model, *args, **kwargs):
#     print(action)
#     if action == 'post_save':
#         print(action)
#         print(instance.title)
#         print("ccccccccccccccccccccccc")
#         # for x in instance.other_author.all():
#         #     print(x.username)



# class PostBackup(models.Model):
#     post = models.ForeignKey(
#         Post,
#         on_delete=models.CASCADE,
#         related_name='post_backup'
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='author_post_backup'
#     )
#     title = models.CharField(
#         max_length=250
#     )
#     body = models.TextField()
#     created = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

    

# @receiver(post_save, sender=Post)
# def post_save_receiver(sender, instance, created, *args, **kwargs):

#     if created:
#         print(instance.id, " Created")
    
#     else:
#         print(instance.id, " was just saved and have a backup")
#         PostBackup.objects.create(
#             post_id=instance.id,
#             author_id=instance.author.id,
#             title=instance.title,
#             body=instance.body
#         )

# from django.core.exceptions import ObjectDoesNotExist

# @receiver(post_save, sender=Post)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         print("Hello ", instance.title)


# @receiver(post_save, sender=Post)
# def save_profile(sender, instance,  **kwargs):
#     try:
#         # instance.profile.save()
#         print("save", instance.title)
#     except ObjectDoesNotExist:
#         Profile.objects.create(user=instance)
#         print("objects not exists yet wait i am creating", instance.title)


class SharedOrOtherEdit(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='others_edited_posts',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    editor = models.ForeignKey(
        User,
        related_name='share_editor',
        on_delete=models.CASCADE
    )
    body = models.TextField()
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edit_summary = models.CharField(max_length=500)

    def __str__(self):
        return self.title

