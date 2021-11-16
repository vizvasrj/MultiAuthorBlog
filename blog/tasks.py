
from celery import shared_task
from django.views.decorators.http import require_GET
from translates.hindi_translate.tasks import hindi_translate
from translates.french_translate.tasks import french_translate
from translates.chinese_translate.tasks import chinese_translate
from translates.spanish_translate.tasks import spanish_translate
from translates.arabic_translate.tasks import arabic_translate, text_to_category
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
from translates.english_translate.tasks import english_translate

from django.contrib.auth.models import User
from .models import MyCustomTag, TagNameValue, Post
from django.db.models import F
from celery import shared_task

from bs4 import BeautifulSoup
import os
from google.cloud import texttospeech, texttospeech_v1
from django.core.files import File
from pydub import AudioSegment
from langdetect import detect

def lang_detect(text, pk):
    ln = detect(text)
    # if ln == 'en':
        # return 

    # french_translate(pk)
    if ln != 'fr':
        french_translate(pk)

    # hindi_translate(pk)
    if ln != 'hi':
        hindi_translate(pk)

    # chinese_translate(pk)
    if ln != 'zh-cn':
        chinese_translate(pk)

    # spanish_translate(pk)
    if ln != 'es':
        spanish_translate(pk)

    # arabic_translate(pk)
    if ln != 'ar':
        arabic_translate(pk)

    # indonesian_translate(pk)
    if ln != 'id':
        indonesian_translate(pk)

    # portuguese_translate(pk)
    if ln != 'pt':
        portuguese_translate(pk)

    # japanese_translate(pk)
    if ln != 'ja':
        japanese_translate(pk)

    # russian_translate(pk)
    if ln != 'ru':
        russian_translate(pk)

    # german_translate(pk)
    if ln != 'de':
        german_translate(pk)

    # korean_translate(pk)
    if ln != 'ko':
        korean_translate(pk)

    # norwegian_translate(pk)
    if ln != 'no':
        norwegian_translate(pk)

    # vietnamese_translate(pk)
    if ln != 'vi':
        vietnamese_translate(pk)

    # filipino_translate(pk)
    if ln != 'ta':
        filipino_translate(pk)

    # italian_translate(pk)
    if ln != 'it':
        italian_translate(pk)

    # english_translate(pk)
    if ln != 'en':
        english_translate(pk)
    return ln


def text_to_speech(text, pk, part=None, ln=None):
    client = texttospeech_v1.TextToSpeechClient()
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    print(ln,"inside text_To_speech")

    # # for Spanish
    if ln == 'es':
        print(ln,"inside es")
        print(text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'es-US',
            name = 'es-US-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for Arabic
    elif ln == 'ar':
        print("inside ar")
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'ar-XA',
            name = 'ar-XA-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for Chinese
    elif ln == 'zn-cn':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'cmn-CN',
            name = 'cmn-CN-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )


    # # for English
    elif ln == 'en':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'en-GB',
            name = 'en-GB-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )
    
    # # for Filipino
    elif ln == 'ta':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'fil-PH',
            name = 'fil-PH-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for French
    elif ln == 'fr':
        print("inside french")
        voice = texttospeech.VoiceSelectionParams(
            language_code = 'fr-FR',
            name = 'fr-FR-Wavenet-E',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for German
    elif ln == 'de':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'de-DE',
            name = 'de-DE-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for Indonasian
    elif ln == 'id':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'id-ID',
            name = 'id-ID-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for Italian
    elif ln == 'it':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'it-IT',
            name = 'it-IT-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for Japanese
    elif ln == 'ja':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'ja-JP',
            name = 'ja-JP-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )


    # # for Korean
    elif ln == 'ko':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'ko-KR',
            name = 'ko-KR-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )


    # # for Norwegian
    elif ln == 'no':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'nb-NO',
            name = 'nb-NO-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )


    # # for Portguese
    elif ln == 'pt':
        print("inside pt")
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'pt-PT',
            name = 'pt-PT-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )
    

    # # for Russian
    elif ln == 'ru':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'ru-RU',
            name = 'ru-RU-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )


    # # for Hindi
    elif ln == 'hi':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'hi-IN',
            name = 'hi-IN-Wavenet-E',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # for Vietnamese
    elif ln == 'vi':
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'vi-VN',
            name = 'vi-VN-Wavenet-A',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    # # For other unknown
    else:
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code = 'en-US',
            name = 'en-US-Wavenet-E',
            ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
        )

    print(voice)

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input = synthesis_input,
        voice = voice,
        audio_config = audio_config
    )
    if part != None:
            
        with open(f'{pk}_{part}_speech.mp3', 'wb') as output:
            output.write(response.audio_content) 
        
    if part == None:
        with open(f'{pk}_speech.mp3', 'wb') as output:
            output.write(response.audio_content) 



def eng_speech(pk):
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
    join = ''.join(map(str, list))
    bs_wp = BeautifulSoup(join, 'html.parser')
    p_title = soup.new_tag("title")
    p_title.string = post.title
    bs_wp.insert(0, p_title)
    p_tags = soup.new_tag("tags")
    p_tags.string = ','.join(tags)
    bs_wp.append(p_tags)
    bs_wp = str(bs_wp).replace("</p>", ".</p>").replace("</title>", ".</title>")

    t_t_n = bs_wp

    for key, value in codes.items():
        t_t_n = t_t_n.replace(key, '')

    r_pre = BeautifulSoup(t_t_n, 'html.parser')
    only_text = r_pre.get_text()
    # language detect  only 500 character
    ln = lang_detect(text = only_text[:500].rsplit(' ', 1)[0], pk=pk)
    if len(only_text) > 5000:
        para = only_text
        text = []
        for p in para.split(". "):
            text.append(p)
        import math
        k = int(math.ceil(len(text)/5))
        split_point = [i for i in range(0, len(text), k)]
        parts = [text[ind:ind+k]for ind in split_point]
        for x in range(len(parts)):
            text_to_speech(text="".join(parts[x]), pk=pk, part=x, ln=ln)



    else:
        t_t_sp = text_to_speech(text=only_text, pk=pk, ln=ln)
    
    try:
        if parts != None:
            audio = []
            for x in range(len(parts)):
                audio.append(f"AudioSegment.from_mp3(f'{pk}_{x}_speech.mp3')")
            join = "+".join(audio)
            "mix_audio = " + join
            executes=("mix_audio = " + join)
            executes2=(f"mix_audio.export('{pk}_speech.mp3')")
            exec(executes)
            exec(executes2)
            
            # mix_audio.export("{pk}_speech.mp3")
            rm_audio = []
            for x in range(len(parts)):
                import os
                os.system(f'rm {pk}_{x}_speech.mp3')
    except:
        pass

    file = open(f'{pk}_speech.mp3', 'rb')
    fileU = File(file)
    
    # h = Post.objects.create(
    #     post_id=pk,
    #     title=str(t_p_title),
    #     # title=post.title,
    #     body=str(t_t_p_s),
    #     audio=fileU
    # )
    post.audio = fileU
    post.save()
    import os
    os.system(f'rm {pk}_speech.mp3')
    # for t_s in t_k_l:
    #     h.tags.add(t_s)
    
    # return t_t_p_s

# def print_title(pk):
@shared_task
def translate_post(pk):
    import time
    time.sleep(2)
    eng_speech(pk=pk)

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
    # italian_translate(pk)
    # english_translate(pk)


# @shared_task
# def add_admin_to_publication(pk):
#     import time
#     time.sleep(2)
#     pub = Publication.objects.get(id=pk)
#     pub.editor.add(pub.admin)
#     return True


def tag_val_inc(user, slug):
    try:
            
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
    except User.DoesNotExist:
        pass

@shared_task
def tag_main(user, post):
    post = Post.objects.get(id=post)
    for tag in post.tags.all():
        tag_val_inc(user=user, slug=tag.slug)
