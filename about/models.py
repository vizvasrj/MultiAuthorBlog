from autoslug.fields import AutoSlugField
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsTextField
from django.contrib.contenttypes.fields import GenericRelation

from account.models import Profile
from comment.models import Comment
from taggit_autosuggest.managers import TaggableManager
from parler.models import TranslatableModel, TranslatedFields


# Create your models here.
class AboutPost(TranslatableModel):
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
        related_name='about_posts',
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
    