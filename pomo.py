import subprocess
from google.cloud import translate
import polib
import json
import os
import time


LANGUAGES = {
    'ar': 'ar',
    'zh_hans': 'zh-CN',
    'ta': 'fil',
    'fr': 'fr',
    'de': 'de',
    'hi': 'hi',
    'id': 'id',
    'it': 'it',
    'ja': 'ja',
    'ko': 'ko',
    'nn': 'no',
    'pt': 'pt-BR',
    'ru': 'ru',
    'es': 'es',
    'vi': 'vi',
}

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/root/Documents/serviceacc.json'


def translate_text(text, code, project_id="cedar-unison-331205"):
    print(code)
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/html",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": code,
        }
    )
    for translation in response.translations:
        return translation.translated_text


proc = subprocess.Popen(
    ['find -L . -maxdepth 6 -name  "*django.po*" -print -type l'], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

# out.split('\n')

for x in out.decode('utf8').split('\n'):
    if x != '':
        # print(x)
        with open(str(x)) as dp:
            text = dp.read()
        out_text = text.split("\n\n")[0]
        type(x)
        print(x)
        try:
            po = polib.pofile(x)
        except:
            pass
        # print(po)
        time.sleep(5)
        e = []
        ln_code = x.split('/')[2]
        if ln_code in LANGUAGES:
            pass
        else:
            ln_code = x.split('/')[3]
        for entry in po:
            e.append(str(polib.POEntry(
                msgid=entry.msgid,
                msgstr=translate_text(text=entry.msgid, code=ln_code),
                occurrences=entry.occurrences
            )))

        joined = '\n'.join(e)

        ff = out_text+'\n\n'+joined
        with open(x, 'w') as tr:
            tr.write(ff)
        # moname = x[:-3]+".mo"
        # po = polib.pofile(x)
        # po.save_as_mofile(moname)

def make_noise():
    duration = 2
    freq = 4400
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq)
)
make_noise()