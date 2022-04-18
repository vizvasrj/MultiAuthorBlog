from autoslug.fields import AutoSlugField
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsTextField
from django.contrib.contenttypes.fields import GenericRelation

from account.models import Profile
from comment.models import Comment
from taggit_autosuggest.managers import TaggableManager
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

# Create your models here.
class AboutPost(models.Model):
    CATEGORY = (
        ('privacy_policy', 'Privacy Policy'),
        ('about_us', 'About Us'),
        ('terms_and_condt', 'Term & Condt.'),
        ('contact_us', 'Contact Us',),
        ('disclaimer', 'Disclaimer'),
        ('cookie_policy', 'Cookie Policy'),
    )
    title = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='title', editable=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    author = models.ForeignKey(
        Profile,
        related_name='about_posts',
        on_delete=models.PROTECT
    )
    cover = models.ImageField(
        upload_to='about/images/',
        blank=True, null=True
    )
    category = models.CharField(max_length=30, choices=CATEGORY, default='c')
    comments = GenericRelation(Comment)
    comment_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "about_post_detail", 
            args=[self.slug]
            )
    

class AboutPostTranslated(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=256, db_index=True),
        slug = models.SlugField(max_length=256, db_index=True),
        body = EditorJsTextField()
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    author = models.ForeignKey(
        Profile,
        related_name='t_about_posts',
        on_delete=models.PROTECT
    )
    cover = models.ImageField(
        upload_to='about/images/',
        blank=True, null=True
    )
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "about_post_detail", 
            args=[self.slug]
            )
    