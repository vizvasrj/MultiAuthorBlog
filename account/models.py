from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


from colorfield.fields import ColorField
from django.db.models.signals import (
    post_save, m2m_changed, pre_save
)
from django.dispatch import receiver
from .tasks import print_full_name
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

class Theme(models.Model):
    name = models.CharField(max_length=50)
    header = ColorField(format='hexa')
    sidebar = ColorField(format='hexa')
    text = ColorField(format='hexa')
    menu = ColorField(format='hexa')
    selected = ColorField(format='hexa')
    hover_background = ColorField(format='hexa')
    hover_text = ColorField(format='hexa')
    image = models.FileField(upload_to='theme', validators=[FileExtensionValidator(['svg'])])

    def __str__(self):
        return self.name



class Profile(models.Model):

    LANGUAGES = (
        ('en', 'English'),
        ('ar', 'عربي'),
        ('zh_hans', '简体中文'),
        ('ta', 'Filipino'),
        ('fr', 'français'),
        ('de', 'Deutsch'),
        ('hi', 'हिंदी'),
        ('id', 'bahasa Indonesia'),
        ('it', 'Italiana'),
        ('ja', '日本'),
        ('ko', '한국인'),
        ('nn', 'Norsk'),
        ('pt', 'Português'),
        ('ru', 'русский'),
        ('es', 'Española'),
        ('vi', 'Tiếng Việt'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profiles',
        verbose_name=_("user")
    )
    full_name = models.CharField(
        _("full name"),
        max_length=100,
        blank=True,
        null=True
    )
    photo = models.ImageField(
        _("photo"),
        upload_to='users/%Y/%m/%d',
        blank=True,
        default='account/defaultprofileimage.jpg'
    )
    about = models.CharField(
        _("about"),
        max_length=150,
        blank=True,
        null=True
    )
    color = ColorField(
        format='hexa'
    )
    lang = models.CharField(
        max_length=10,
        choices=LANGUAGES,
        default='en'
    )
    my_theme = models.ForeignKey(
        Theme,
        related_name='themes',
        on_delete=models.CASCADE,
        default=1,
        verbose_name=_("my theme")
    )
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return self.user



@receiver(post_save, sender=Profile)
def post_save_receiver(sender, created, instance, *args, **kwargs):

    if created:
        # print("created did slug changed?")
        pass
    else:
        # print("updated", instance.full_name)
        pass
        # print_full_name.delay(name=instance.full_name)
        


class Contact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='rel_from_set',
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        User,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
    )
)



