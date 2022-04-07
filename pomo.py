import subprocess
from threading import Thread
# from google.cloud import translate
import polib
import json
import os
import time
from django.conf import settings
from deep_translator import GoogleTranslator

LANGUAGES = {
    'ar': 'ar',
    'zh_Hans': 'zh-CN',
    'tl': 'tl',
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


# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_SERVICE_KEY


# def translate_text(text, code, project_id="cedar-unison-331205"):
#     print(code)
#     client = translate.TranslationServiceClient()
#     location = "global"
#     parent = f"projects/{project_id}/locations/{location}"
#     response = client.translate_text(
#         request={
#             "parent": parent,
#             "contents": [text],
#             "mime_type": "text/html",  # mime types: text/plain, text/html
#             # "source_language_code": "en-US",
#             "target_language_code": code,
#         }
#     )
#     for translation in response.translations:
#         return translation.translated_text


def translate_text(text, code):
    return GoogleTranslator(source='auto', target=code).translate(text)

# proc = subprocess.Popen(
#     ['find -L . -maxdepth 6 -name  "*django.po*" -print -type l'], stdout=subprocess.PIPE, shell=True)
# (out, err) = proc.communicate()

# out.split('\n')

# for x in out.decode('utf8').split('\n'):
#     if x != '':
#         # print(x)
#         with open(str(x)) as dp:
#             text = dp.read()
#         out_text = text.split("\n\n")[0]
#         type(x)
#         print(x)
#         try:
#             po = polib.pofile(x)
#         except OSError:
#             pass
#         # print(po)
#         time.sleep(5)
#         e = []
#         ln_code = x.split('/')[2]
#         if ln_code in LANGUAGES:
#             pass
#         else:
#             ln_code = x.split('/')[3]
#         for entry in po:
#             e.append(str(polib.POEntry(
#                 msgid=entry.msgid,
#                 msgstr=translate_text(text=entry.msgid, code=ln_code),
#                 occurrences=entry.occurrences
#             )))

#         joined = '\n'.join(e)

#         ff = out_text+'\n\n'+joined
#         with open(x, 'w') as tr:
#             tr.write(ff)
        # moname = x[:-3]+".mo"
        # po = polib.pofile(x)
        # po.save_as_mofile(moname)

# def make_noise():
#     duration = 2
#     freq = 4400
#     os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
# make_noise()


import os
import sys
args = sys.argv
from termcolor import colored
import itertools
from multiprocessing.dummy import Pool as ThreadPool


def create_po():
    null = []
    print(args[1:])
    if args[1:]:
        for x in args[1:]:
            if x == 'all':
                pool = ThreadPool(10)
                results = pool.starmap(translate_text, zip(itertools.chain(LANGUAGES)))
                pool.close()
                pool.join()
                return results
            else:
                try:
                    ln = LANGUAGES[x]
                except KeyError:
                    error = {
                        'language': x,
                        'error': KeyError
                    }
                    print(x, "KEY ERROR")
                    null.append(error)
                    continue
                p = os.popen('find -L . -maxdepth 6 -name  "*django.po*" -print -type l|grep "/'+x+'/"').read().strip()
                if len(p) == 0:
                    null.append(x)
                else:
                    print(p)
                    mo = "/".join(p.split('/')[:-1])
                    dext = p.split('/')[-1]
                    ext = dext.split('.')[0]
                    namext = '/'+ext+'.bk'
                    nemo = mo + namext
                    print(nemo)
                    po = polib.pofile(p)
                    for entry in po:
                        entry.msgstr = translate_text(text=entry.msgid, code=ln)
                        print(entry.msgstr)
                        print(entry.msgid)
                    po.save(nemo)
                    os.popen('mv '+nemo+' '+p)

    if null is []:
        pass
    else:
        print(colored(null, 'red'), "DID not return Good PLz check name")

