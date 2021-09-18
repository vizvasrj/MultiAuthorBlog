
from celery import shared_task
from hindi_translate.tasks import hindi_translate
from french_translate.tasks import french_translate
from chinese_translate.tasks import chinese_translate
from spanish_translate.tasks import spanish_translate
from arabic_translate.tasks import arabic_translate
from indonesian_translate.tasks import indonesian_translate
from portuguese_translate.tasks import portuguese_translate
from japanese_translate.tasks import japanese_translate
from russian_translate.tasks import russian_translate
from german_translate.tasks import german_translate
from korean_translate.tasks import korean_translate
from norwegian_translate.tasks import norwegian_translate
from vietnamese_translate.tasks import vietnamese_translate
from filipino_translate.tasks import filipino_translate
from italian_translate.tasks import italian_translate


from celery import shared_task
@shared_task
def print_title(pk):
    import time
    time.sleep(2)
    french_translate(pk)
    hindi_translate(pk)
    chinese_translate(pk)
    spanish_translate(pk)
    arabic_translate(pk)
    indonesian_translate(pk)
    portuguese_translate(pk)
    japanese_translate(pk)
    russian_translate(pk)
    german_translate(pk)
    korean_translate(pk)
    norwegian_translate(pk)
    vietnamese_translate(pk)
    filipino_translate(pk)
    italian_translate(pk)
