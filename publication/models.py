from django.db import models
from django.contrib.auth.models import User
# 3rd party
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from django.urls import reverse


class Publication(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='publication',
        null=True
    )
    slug = AutoSlugField(populate_from='name')
    tags = TaggableManager()
    publisher  = models.ForeignKey(
        User,
        related_name='publications',
        on_delete=models.CASCADE
    )
    editors = models.ManyToManyField(
        User,
        related_name='publications_editors'
    )
    about = models.TextField()
    followers = models.ManyToManyField(
        User,
        through='PublicationContact',
        related_name='publications_following',
        symmetrical=False
    )
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publication_detail", kwargs={"slug": self.slug})
