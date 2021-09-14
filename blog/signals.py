from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, m2m_changed, pre_save
)
from django.utils.text import slugify
from django.core.signals import request_finished

from polyglot.detect import Detector
from unidecode import unidecode

from .models import Post

# the translate function importing

@receiver(m2m_changed, sender=Post.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
    

# only once 
@receiver(pre_save, sender=Post)
def pre_save_receiver(sender, instance, created=False,  *args, **kwargs):
    if instance._state.adding:
            
        last_id = Post.objects.latest('id').id + 1
        # ln as language code
        # ln = Detector(instance.title).language.code
        ln = 'en'
        # unidecode to change it from slug of diffrent language other
        # than english to slug
        instance.slug = f'{slugify(unidecode(instance.title))}-{hex(last_id)}-{ln}'

        # This will be used to translate and speech translation

    else:
        print("Only updating")