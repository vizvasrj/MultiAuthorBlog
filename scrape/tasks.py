from celery import shared_task
from account.models import Profile
from scrape.models import HealthlineParsed

from blog.models import Post
from bs4 import BeautifulSoup
import os
from google.cloud import (
    translate,
    texttospeech_v1,
    texttospeech
)
import random
from termcolor import colored


from django.conf import settings
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_SERVICE_KEY

def translate_text(text, project_id=settings.GOOGLE_PROJECT_ID):
    # Translating text
    client = translate.TranslationServiceClient()
    location = 'global'
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/html",  # mime types: text/plain, text/html
            # "source_language_code": "en-US",
            "target_language_code": "hi",
        }
    )
    for translation in response.translations:
        return translation.translated_text



@shared_task
def hi_only_translate(pk):
    post = HealthlineParsed.objects.get(id=pk)
    body = post.description
    title = post.title
    # tags = []
    # for tag in post.tags.all():
    #     tags.append(tag.name)

    soup = BeautifulSoup(body, 'html.parser')
    bs_wp = BeautifulSoup(str(soup), 'html.parser')
    p_title = soup.new_tag("title")
    p_title.string = title
    bs_wp.insert(0, p_title)
    # p_tags = soup.new_tag("tags")
    # p_tags.string = ','.join(tags)
    # bs_wp.append(p_tags)
    t_t = translate_text(text=str(bs_wp))
    t_t_p_s = BeautifulSoup(t_t, 'html.parser')
    print(colored(t_t_p_s, "blue"))
    tag_title = t_t_p_s.title
    t_p_title = tag_title.string
    tag_title.decompose()
    # tag_keys = t_t_p_s.tags
    # t_p_keys = tag_keys.string
    # print(t_p_keys)
    # t_k_l = t_p_keys.split(',')
    # tag_keys.decompose()

    profile = Profile.objects.order_by("?").exclude(user=1)[0]
    h = Post.objects.create(
        title=str(t_p_title),
        body=str(t_t_p_s),
        author=profile
    )
    print(colored(h, "red"))
    # for t_s in t_k_l:
    #     h.tags.add(t_s)
