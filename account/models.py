from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


from colorfield.fields import ColorField
from django.db.models.signals import (
    post_save, m2m_changed, pre_save
)
from django.dispatch import receiver
from .tasks import print_full_name

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d',
        blank=True,
        default='account/defaultprofileimage.jpg'
    )
    full_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    about = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    color = ColorField(
        format='hexa'
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return self.user



@receiver(post_save, sender=Profile)
def post_save_receiver(sender, created, instance, *args, **kwargs):

    if created:
        print("created did slug changed?")
    else:
        print("updated", instance.full_name)
        print_full_name.delay(name=instance.full_name)
        


class Contact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='rel_from_set',
        on_delete=models.CASCADE
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


