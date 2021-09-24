from django.dispatch import receiver
from django.db.models.signals import (
    pre_save, post_save
)
from django.utils.text import slugify

from .models import RussianTranslatedPost

from unidecode import unidecode
from django.core.exceptions import ObjectDoesNotExist


# This will run at first time only
# when post is created
# 
@receiver(pre_save, sender=RussianTranslatedPost)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if instance._state.adding:
        try:
            last_id = RussianTranslatedPost.objects.latest('id').id + 1
        except ObjectDoesNotExist:
            last_id = 0 + 1
        instance.slug = f'{slugify(unidecode(instance.title))}-{hex(last_id)}-ru'
    else:
        pass