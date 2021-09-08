from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, m2m_changed
)

from .models import Post


@receiver(m2m_changed, sender=Post.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
    

# @receiver(m2m_changed, sender=Post.other_author.through)
# def other_auther_changed(sender, *args, **kwargs):
#     print(sender, args, kwargs)

# @receiver(m2m_changed, sender=Post.users_like.through)
# def user_liked_changed(sender, *args, **kwargs):
#     print(sender, *args, *kwargs)
#     print("Not working")

# @receiver(post_save, sender=Post)
# def post_save_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("Send email to ", instance.author)
#         instance.save()
#     else:
#         print(instance.title, " was just saved")
