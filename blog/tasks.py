
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

from blog.models import Publication


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


@shared_task
def add_admin_to_publication(pk):
    import time
    time.sleep(2)
    pub = Publication.objects.get(id=pk)
    pub.editor.add(pub.admin)
    return True