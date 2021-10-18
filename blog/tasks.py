
from celery import shared_task
from translates.hindi_translate.tasks import hindi_translate
from translates.french_translate.tasks import french_translate
from translates.chinese_translate.tasks import chinese_translate
from translates.spanish_translate.tasks import spanish_translate
from translates.arabic_translate.tasks import arabic_translate
from translates.indonesian_translate.tasks import indonesian_translate
from translates.portuguese_translate.tasks import portuguese_translate
from translates.japanese_translate.tasks import japanese_translate
from translates.russian_translate.tasks import russian_translate
from translates.german_translate.tasks import german_translate
from translates.korean_translate.tasks import korean_translate
from translates.norwegian_translate.tasks import norwegian_translate
from translates.vietnamese_translate.tasks import vietnamese_translate
from translates.filipino_translate.tasks import filipino_translate
from translates.italian_translate.tasks import italian_translate


from django.contrib.auth.models import User
from .models import MyCustomTag, TagNameValue, Post
from django.db.models import F
from celery import shared_task

@shared_task
# def print_title(pk):
def translate_post(pk):
    import time
    time.sleep(2)
    # french_translate(pk)
    # hindi_translate(pk)
    # chinese_translate(pk)
    # spanish_translate(pk)
    # arabic_translate(pk)
    # indonesian_translate(pk)
    # portuguese_translate(pk)
    # japanese_translate(pk)
    # russian_translate(pk)
    # german_translate(pk)
    # korean_translate(pk)
    # norwegian_translate(pk)
    # vietnamese_translate(pk)
    # filipino_translate(pk)
    italian_translate(pk)


# @shared_task
# def add_admin_to_publication(pk):
#     import time
#     time.sleep(2)
#     pub = Publication.objects.get(id=pk)
#     pub.editor.add(pub.admin)
#     return True


def tag_val_inc(user, slug):
    user = User.objects.get(id=user)
    tag = MyCustomTag.objects.get(slug=slug)
    tag_name = TagNameValue.objects.filter(tag__slug=slug, user=user)
    if tag_name.exists():
        tag_name.update(value=F('value')+1)
    else:
        tag_name = TagNameValue.objects.get_or_create(
            tag=tag,
            user=user,
            value=1
        )
    return True

@shared_task
def tag_main(user, post):
    post = Post.objects.get(id=post)
    for tag in post.tags.all():
        tag_val_inc(user=user, slug=tag.slug)
