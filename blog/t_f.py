import os
from google.cloud import (
    texttospeech, texttospeech_v1, translate
)
from bs4 import BeautifulSoup
# from hindi_translate.models import HindiTranslatedPost


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceacc.json'




def post_to_exclude_pre(body):
    soup = BeautifulSoup(body, 'html.parser')
    codes = {}
    count = 1000
    for x in soup:
        if x.name == 'pre':
            count += 1
            love = f'00-00-{count}'
            codes[love] = x
            print(love)
            return f'{love} '

        else:
            print(x)
            return f'{x}'

    