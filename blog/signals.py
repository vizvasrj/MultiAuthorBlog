from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, m2m_changed, pre_save
)
from django.utils.text import slugify
from django.core.signals import request_finished


from unidecode import unidecode

from .models import Post
from .tasks import translate_post
# the translate function importing


# @receiver(post_save, sender=Publication)
# def post_save_receiver(sender, created, instance, *args, **kwargs):

#     if created:
#         add_admin_to_publication.delay(pk=instance.id)



@receiver(m2m_changed, sender=Post.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
    

# only once 
@receiver(pre_save, sender=Post)
def pre_save_receiver(sender, instance, created=False,  *args, **kwargs):
    if instance._state.adding:
        try:

            last_id = Post.objects.latest('id').id + 1
        except Post.DoesNotExist:
            last_id = 1
        # ln as language code
        # ln = 'en'
        # unidecode to change it from slug of diffrent language other
        # than english to slug
        instance.slug = f'{slugify(unidecode(instance.title))}-{hex(last_id)}'
        # print("#33##################")
        
        # print(instance.title)
        # print("#33##################")

        # This will be used to translate and speech translation

    else:
        # print("Only updating")
        # no translation for now
        print("Update posts")
        # translate_post.delay(pk=instance.id)
        
        # for x in instance.tags.all():
        #     print(x)
        # pass


        

"""
This is translator of blog
"""
@receiver(post_save, sender=Post)
def post_save_receiver(sender, created, instance, *args, **kwargs):

    if created:
        print("created <post save>")

        translate_post.delay(pk=instance.id)
        print("created did slug changed?")
        # mail = mail_post.delay(post_id=instance.id, title=instance.title, status=instance.status)
        # print(mail)
        print(instance.slug, " was just saved")


