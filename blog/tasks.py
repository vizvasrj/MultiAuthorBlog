# bs_wp BeautifulSoup Without pre tag
# t_t = translated_text ie def translate_text()
# t_t_n = translated_Text_replace 00-00 data to null
# t_t_n_s is translated text null beautifulsoup
# t_t_n_s_t is translated text null beautifulsoup only text
# t_t_sp = translated text speech
# t_t_p = translated text with pre tag
# t_t_p_c = translated_text_with_pre_content
# t_p_title = translated_post_title
# t_p_keys = translated_post_keys/tags/taggit
# t_k_l =  translated_keys_list
# t_s = tag_seperated
from celery import shared_task
from .models import Post
from hindi_translate.models import HindiTranslatedPost
from bs4 import BeautifulSoup
import os
from google.cloud import (
    translate,
    texttospeech_v1,
    texttospeech
) 
from google.cloud import language_v1

from django.core.files import File
from pydub import AudioSegment

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/root/Project/texttospeech/speech/serviceacc.json'


def translate_text(text, project_id="quick-yen-321916"):
    # Translating text
    client = translate.TranslationServiceClient()
    location = 'global'
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/html",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "hi",
        }
    )
    for translation in response.translations:
        return translation.translated_text

def text_to_category(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.HTML)
    response = client.analyze_entities(document=document, encoding_type='UTF32')
    
    return response.entities


def text_to_speech(text, pk, part=None):
    client = texttospeech_v1.TextToSpeechClient()
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code = 'en-IN',
        name = 'en-IN-Wavenet-D',
        ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input = synthesis_input,
        voice = voice,
        audio_config = audio_config
    )
    if part == 1:

        with open(f'{pk}_1.mp3', 'wb') as output:
            output.write(response.audio_content) 
    if part == 2:
        with open(f'{pk}_2.mp3', 'wb') as output:
            output.write(response.audio_content)
        sound1 = AudioSegment.from_mp3(f'{pk}_1.mp3')
        sound2 = AudioSegment.from_mp3(f'{pk}_2.mp3')
        sound3 = sound1 + sound2
        sound3.export(f'{pk}.mp3')
        os.system(f'rm {pk}_2.mp3')
        os.system(f'rm {pk}_1.mp3')
        
    if part == None:
        with open(f'{pk}.mp3', 'wb') as output:
            output.write(response.audio_content) 
        

@shared_task
def print_title(pk):
    print(pk)
    import time
    time.sleep(2)
    post = Post.objects.get(id=pk)
    body = post.body
    title = post.title
    tags = []
    for tag in post.tags.all():
        tags.append(tag.name)
    
    soup = BeautifulSoup(body, 'html.parser')
    codes = {}
    count = 1000
    list = []
    for x in soup:
        if x.name == 'pre':
            count += 1
            love = f'00-00-{count}'
            codes[love] = x
            list.append(f'{str(love)} ')
        else:
            list.append(f'{str(x)} ')
    join = "".join(map(str, list))
    bs_wp = BeautifulSoup(join, 'html.parser')
    # title and tags are added so they can be trans-
    # lated
    p_title = soup.new_tag("title")
    p_title.string = post.title
    bs_wp.insert(0, p_title)
    p_tags = soup.new_tag("tags")
    p_tags.string = ",".join(tags)

    bs_wp.append(p_tags)
    t_c = text_to_category(text=str(bs_wp))
    print (t_c[0].name)

    t_t = translate_text(text=str(bs_wp))

    # speech need only text, replace with null
    t_t_n = t_t
    for key, value in codes.items():
        t_t_n = t_t_n.replace(str(key), '')

    t_t_n_s = BeautifulSoup(t_t_n, 'html.parser')
    t_t_n_s_t = t_t_n_s.get_text()
    # speech takes only 5000 character
    l_s = []
    if len(t_t_n_s_t) > 5000:
        for s_s in t_t_n_s_t.split(","):
            l_s.append(s_s)
        length = len(l_s)
        middle_index = length//2
        first_half = l_s[:middle_index]
        second_half = l_s[middle_index:]
        first_half = ". ".join(map(str, first_half))
        second_half = ". ".join(map(str, second_half))
        text_to_speech(text=first_half, pk=pk, part=1)
        text_to_speech(text=second_half, pk=pk, part=2)

    else:
        t_t_sp = text_to_speech(text=t_t_n_s_t, pk=pk)
    # before uploading to hindi_tra.. replace it with pre
    t_t_p = t_t
    for ke, val in codes.items():
        t_t_p = t_t_p.replace(str(ke), str(val))
    # print(t_t_p)
    t_t_p_s = BeautifulSoup(t_t_p, 'html.parser')
    print(t_t_p_s)
    tag_title = t_t_p_s.title
    # print(title)
    t_p_title = tag_title.string
    tag_title.decompose()
    tag_keys = t_t_p_s.tags
    t_p_keys = tag_keys.string
    print(t_p_keys)
    t_k_l = t_p_keys.split(',')
    tag_keys.decompose()

    t_t_p_c = t_t_p

    # saving to translate models ie Hindi
    file = open(f'{pk}.mp3', 'rb')
    fileU = File(file)
    
    h = HindiTranslatedPost.objects.create(
        post_id=pk,
        title=str(t_p_title),
        # title=post.title,
        body=str(t_t_p_s),
        audio=fileU
    )
    import os
    os.system(f'rm {pk}.mp3')
    for t_s in t_k_l:
        h.tags.add(t_s)
    
    return t_t_p_s
