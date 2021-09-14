from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from account.models import Profile
# from about.models import AboutPost

class Comment(MPTTModel):
    # about_post = models.ForeignKey(
    #     AboutPost,
    #     related_name='comments',
    #     on_delete=models.CASCADE
    # )
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    commentor = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        null=True,
        related_name='user_comment'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='child'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    users_like = models.ManyToManyField(
        User,
        related_name='comment_liked',
        blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )
    class MPTTMeta:
        order_instertion_by = ['publish']

    def __str__(self):
        return self.body[:20]

