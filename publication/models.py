from django.db import models
from django.contrib.auth.models import User
# 3rd party
from autoslug import AutoSlugField
from taggit_autosuggest.managers import TaggableManager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Publication(models.Model):
    name = models.CharField(_("name"), max_length=50)
    image = models.ImageField(
        _('image'),
        upload_to='publication',
        null=True
    )
    slug = AutoSlugField(_('slug'), populate_from='name')
    tags = TaggableManager(
        related_name='publications_tag',
        verbose_name=_('tags')
    )
    publisher  = models.ForeignKey(
        User,
        related_name='publications',
        on_delete=models.CASCADE,
        verbose_name=_('publisher')
    )
    writer = models.ManyToManyField(
        User,
        related_name='publications_cc',
        verbose_name=_('writer')
    )
    about = models.TextField(_('about'))
    followers = models.ManyToManyField(
        User,
        through='PublicationContact',
        related_name='p_following',
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


class PublicationContact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='from_user',
        on_delete=models.CASCADE
    )
    to_publication = models.ForeignKey(
        Publication,
        related_name='to_publication',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.to_publication}'

