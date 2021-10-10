from .models import Publication as Pub
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, m2m_changed,
)
from .tasks import add_admin_to_publication


# @receiver(post_save, sender=Pub)
# def post_save_receiver(sender, created, instance, *args, **kwargs):

#     if created:
#         add_admin_to_publication.delay(pk=instance.id)


# @receiver(m2m_changed, sender=Pub.content_creater.through)
# def users_added_changed
