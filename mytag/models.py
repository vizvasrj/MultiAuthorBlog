from django.db import models
from taggit.models import  TagBase, GenericTaggedItemBase, ItemBase, TaggedItemBase
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.urls import reverse

class MyCustomTag(TagBase):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=name)
    creator = models.ForeignKey(
        User,
        related_name='tag_creators',
        on_delete=models.PROTECT,
        default=1,
    )
    original = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(
        User,
        through='TagContact',
        related_name='t_following',
        symmetrical=False
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    # def save(self, *args, **kwargs):
    #     user = get_current_user().id
    #     user = User.objects.get(id=user)
    #     # if not self.pk:
    #     self.creator = user
    #     super(MyCustomTag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tags_posts_lists", kwargs={"slug": self.slug})

class TagContact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='t_from_user',
        on_delete=models.CASCADE
    )
    to_tag = models.ForeignKey(
        MyCustomTag,
        related_name='to_tag',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.to_tag}'


class TaggedWhatever(TaggedItemBase, GenericTaggedItemBase):
    # TaggedWhatever can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(
        MyCustomTag,
        on_delete=models.CASCADE,
        related_name="blogs_posts_items",
    )
    

class TagNameValue(models.Model):

    tag = models.ForeignKey(
        MyCustomTag,  
        on_delete=models.CASCADE,
        related_name='tags_name'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_tag'
    )
    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.tag} in {self.user}'




# Some Stackoverflow
# https://stackoverflow.com/questions/38944551/steps-to-troubleshoot-django-db-utils-programmingerror-permission-denied-for-r
# https://stackoverflow.com/questions/42234330/django-error-on-migration-there-is-no-unique-constraint-matching-given-keys-fo