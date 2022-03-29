
# Create your views here.
import time
import gzip
from django.core.files import File
import os

from blog.models import Post
from sitemap.models import Sitemap
import requests

from translates.hindi_translate.models import HindiTranslatedPost
from translates.arabic_translate.models import ArabicTranslatedPost
from translates.chinese_translate.models import ChineseTranslatedPost
from translates.filipino_translate.models import FilipinoTranslatedPost
from translates.french_translate.models import FrenchTranslatedPost
from translates.german_translate.models import GermanTranslatedPost
from translates.indonesian_translate.models import IndonesianTranslatedPost
from translates.italian_translate.models import ItalianTranslatedPost
from translates.japanese_translate.models import JapaneseTranslatedPost
from translates.korean_translate.models import KoreanTranslatedPost
from translates.norwegian_translate.models import NorwegianTranslatedPost
from translates.portuguese_translate.models import PortugueseTranslatedPost
from translates.russian_translate.models import RussianTranslatedPost 
from translates.spanish_translate.models import SpanishTranslatedPost
from translates.vietnamese_translate.models import VietnameseTranslatedPost
from translates.english_translate.models import EnglishTranslatedPost

# This get_code return language code if exsists for given post
def get_code(post):
    ln = {}
    if post.arabic_translated_post.all().count() > 0:
        tpost = ArabicTranslatedPost.objects.filter(post=post).latest()
        ln["ar"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["ar"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.chinese_translated_post.all().count() > 0:
        tpost = ChineseTranslatedPost.objects.filter(post=post).latest()
        ln["zh-hans"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["zh-hans"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.english_translated_post.all().count() > 0:
        tpost = EnglishTranslatedPost.objects.filter(post=post).latest()
        ln["en"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["en"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.filipino_translated_post.all().count() > 0:
        tpost = FilipinoTranslatedPost.objects.filter(post=post).latest()
        ln["ta"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["ta"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.french_translated_post.all().count() > 0:
        tpost = FrenchTranslatedPost.objects.filter(post=post).latest()
        ln["fr"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["fr"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.german_translated_post.all().count() > 0:
        tpost = GermanTranslatedPost.objects.filter(post=post).latest()
        ln["de"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["de"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.hindi_translated_post.all().count() > 0:
        tpost = HindiTranslatedPost.objects.filter(post=post).latest()
        ln["hi"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["hi"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.indonesian_translated_post.all().count() > 0:
        tpost = IndonesianTranslatedPost.objects.filter(post=post).latest()
        ln["id"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["id"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.italian_translated_post.all().count() > 0:
        tpost = ItalianTranslatedPost.objects.filter(post=post).latest()
        ln["it"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["it"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.japanese_translated_post.all().count() > 0:
        tpost = JapaneseTranslatedPost.objects.filter(post=post).latest()
        ln["ja"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["ja"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.korean_translated_post.all().count() > 0:
        tpost = KoreanTranslatedPost.objects.filter(post=post).latest()
        ln["ko"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["ko"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.norwegian_translated_post.all().count() > 0:
        tpost = NorwegianTranslatedPost.objects.filter(post=post).latest()
        ln["nn"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["nn"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.portuguese_translated_post.all().count() > 0:
        tpost = PortugueseTranslatedPost.objects.filter(post=post).latest()
        ln["pt"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["pt"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.russian_translated_post.all().count() > 0:
        tpost = RussianTranslatedPost.objects.filter(post=post).latest()
        ln["ru"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["ru"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.spanish_translated_post.all().count() > 0:
        tpost = SpanishTranslatedPost.objects.filter(post=post).latest()
        ln["es"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["es"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    if post.vietnamese_translated_post.all().count() > 0:
        tpost = VietnameseTranslatedPost.objects.filter(post=post).latest()
        ln["vi"] = tpost.updated.strftime("%Y-%m-%d")
        # ln["vi"] = f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
    
    return ln

def onethousand(url, date, ln):
    aa = []
    for x in ln:
        
        whole = "https://vizvasrj.com/" + x + "/" + url
        a = '<url xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><loc>' + whole + '</loc><lastmod>' + ln[x]+'</lastmod><changefreq>always</changefreq><priority>0.9</priority></url>'
        data = {
            "lan": x,
            "date": ln[x],
            "url": a,
        }
        aa.append(data)
    return aa


# def sitemap_creator():
sdata = []
for x in range(Post.objects.all()[16000].id):
    try:
        post = Post.objects.get(id=x)
        date = post.updated.strftime("%Y-%m-%d")
        # date=f'{randint(2005,2025)}-{randint(1,12)}-{randint(1,28)}'
        aburl = post.get_absolute_url()
        url = aburl.split('/')[2:]
        jurl = "/".join(url)
        ln = get_code(post)
        sitemap_url = onethousand(jurl, date, ln)
        data = {
            'url': sitemap_url
        }
        sdata.append(data)
    except Post.DoesNotExist:
        pass

# sdata.sort(key=lambda x: x["date"], reverse=True)

start_bracket = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
end_bracket = '</urlset>'
ar = []
zh_hans = []
en = []
ta = []
fr = []
de = []
hi = []
id = []
it = []
ja = []
ko = []
nn = []
pt = []
ru = []
es = []
vi = []

start_time = time.time()
for x in sdata:
    for y in x["url"]:
        if y["lan"] == "ar":
            data = {"date": y["date"], "surl": y["url"]}
            ar.append(data)
        if y["lan"] == "zh-hans":
            data = {"date": y["date"], "surl": y["url"]}
            zh_hans.append(data)
        if y["lan"] == "en":
            data = {"date": y["date"], "surl": y["url"]}
            en.append(data)
        if y["lan"] == "ta":
            data = {"date": y["date"], "surl": y["url"]}
            ta.append(data)
        if y["lan"] == "fr":
            data = {"date": y["date"], "surl": y["url"]}
            fr.append(data)
        if y["lan"] == "de":
            data = {"date": y["date"], "surl": y["url"]}
            de.append(data)
        if y["lan"] == "hi":
            data = {"date": y["date"], "surl": y["url"]}
            hi.append(data)
        if y["lan"] == "id":
            data = {"date": y["date"], "surl": y["url"]}
            id.append(data)
        if y["lan"] == "it":
            data = {"date": y["date"], "surl": y["url"]}
            it.append(data)
        if y["lan"] == "ja":
            data = {"date": y["date"], "surl": y["url"]}
            ja.append(data)
        if y["lan"] == "ko":
            data = {"date": y["date"], "surl": y["url"]}
            ko.append(data)
        if y["lan"] == "nn":
            data = {"date": y["date"], "surl": y["url"]}
            nn.append(data)
        if y["lan"] == "pt":
            data = {"date": y["date"], "surl": y["url"]}
            pt.append(data)
        if y["lan"] == "ru":
            data = {"date": y["date"], "surl": y["url"]}
            ru.append(data)
        if y["lan"] == "es":
            data = {"date": y["date"], "surl": y["url"]}
            es.append(data)
        if y["lan"] == "vi":
            data = {"date": y["date"], "surl": y["url"]}
            vi.append(data)

ar.sort(key=lambda x: x["date"], reverse=True)
zh_hans.sort(key=lambda x: x["date"], reverse=True)
en.sort(key=lambda x: x["date"], reverse=True)
ta.sort(key=lambda x: x["date"], reverse=True)
fr.sort(key=lambda x: x["date"], reverse=True)  
de.sort(key=lambda x: x["date"], reverse=True)
hi.sort(key=lambda x: x["date"], reverse=True)
id.sort(key=lambda x: x["date"], reverse=True)
it.sort(key=lambda x: x["date"], reverse=True)
ja.sort(key=lambda x: x["date"], reverse=True)
ko.sort(key=lambda x: x["date"], reverse=True)
nn.sort(key=lambda x: x["date"], reverse=True)
pt.sort(key=lambda x: x["date"], reverse=True)
ru.sort(key=lambda x: x["date"], reverse=True)
es.sort(key=lambda x: x["date"], reverse=True)
vi.sort(key=lambda x: x["date"], reverse=True)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    d = []
    for i in range(0, len(lst), n):
        d.append(lst[i : i + n])

    return d

ar_url = []
for x in ar:
    ar_url.append(x['surl'])

zh_hans_url = []
for x in zh_hans:
    zh_hans_url.append(x['surl'])

en_url = []
for x in en:
    en_url.append(x['surl'])

ta_url = []
for x in ta:
    ta_url.append(x['surl'])


fr_url = []
for x in fr:
    fr_url.append(x['surl'])


de_url = []
for x in de:
    de_url.append(x['surl'])


hi_url = []
for x in hi:
    hi_url.append(x['surl'])


id_url = []
for x in id:
    id_url.append(x['surl'])

it_url = []
for x in it:
    it_url.append(x['surl'])

ja_url = []
for x in ja:
    ja_url.append(x['surl'])

ko_url = []
for x in ko:
    ko_url.append(x['surl'])

nn_url = []
for x in nn:
    nn_url.append(x['surl'])

pt_url = []
for x in pt:
    pt_url.append(x['surl'])

ru_url = []
for x in ru:
    ru_url.append(x['surl'])

es_url = []
for x in es:
    es_url.append(x['surl'])


vi_url = []
for x in vi:
    vi_url.append(x['surl'])

ar_sitemap = chunks(ar_url, 1000)
zh_hans_sitemap = chunks(zh_hans_url, 1000)
en_sitemap = chunks(en_url, 1000)
ta_sitemap = chunks(ta_url, 1000)
fr_sitemap = chunks(fr_url, 1000)
de_sitemap = chunks(de_url, 1000)
hi_sitemap = chunks(hi_url, 1000)
id_sitemap = chunks(id_url, 1000)
it_sitemap = chunks(it_url, 1000)
ja_sitemap = chunks(ja_url, 1000)
ko_sitemap = chunks(ko_url, 1000)
nn_sitemap = chunks(nn_url, 1000)
pt_sitemap = chunks(pt_url, 1000)
ru_sitemap = chunks(ru_url, 1000)
es_sitemap = chunks(es_url, 1000)
vi_sitemap = chunks(vi_url, 1000)

end_time = time.time() - start_time
print(end_time)

for idx, x in enumerate(ar_sitemap):
    with open(f'ar_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'ar_sitemap_{idx}.xml', 'r'))
        os.remove(f'ar_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'ar_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(zh_hans_sitemap):
    with open(f'zh_hans_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'zh_hans_sitemap_{idx}.xml', 'r'))
        os.remove(f'zh_hans_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'zh_hans_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        

for idx, x in enumerate(en_sitemap):
    with open(f'en_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'en_sitemap_{idx}.xml', 'r'))
        os.remove(f'en_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'en_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(ta_sitemap):
    with open(f'ta_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'ta_sitemap_{idx}.xml', 'r'))
        os.remove(f'ta_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'ta_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(fr_sitemap):
    with open(f'fr_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'fr_sitemap_{idx}.xml', 'r'))
        os.remove(f'fr_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'fr_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(de_sitemap):
    with open(f'de_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'de_sitemap_{idx}.xml', 'r'))
        os.remove(f'de_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'de_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
        
for idx, x in enumerate(hi_sitemap):
    with open(f'hi_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'hi_sitemap_{idx}.xml', 'r'))
        os.remove(f'hi_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'hi_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(id_sitemap):
    with open(f'id_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'id_sitemap_{idx}.xml', 'r'))
        os.remove(f'id_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'id_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(it_sitemap):
    with open(f'it_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'it_sitemap_{idx}.xml', 'r'))
        os.remove(f'it_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'it_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(ja_sitemap):
    with open(f'ja_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'ja_sitemap_{idx}.xml', 'r'))
        os.remove(f'ja_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'ja_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(ko_sitemap):
    with open(f'ko_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'ko_sitemap_{idx}.xml', 'r'))
        os.remove(f'ko_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'ko_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(nn_sitemap):
    with open(f'nn_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'nn_sitemap_{idx}.xml', 'r'))
        os.remove(f'nn_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'nn_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(pt_sitemap):
    with open(f'pt_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'pt_sitemap_{idx}.xml', 'r'))
        os.remove(f'pt_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'pt_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(ru_sitemap):
    with open(f'ru_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'ru_sitemap_{idx}.xml', 'r'))
        os.remove(f'ru_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'ru_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(es_sitemap):
    with open(f'es_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'es_sitemap_{idx}.xml', 'r'))
        os.remove(f'es_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'es_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
for idx, x in enumerate(vi_sitemap):
    with open(f'vi_sitemap_{idx}.xml', 'wb', 5) as f:
        one = start_bracket + "".join(x) + end_bracket            
        f.write(one.encode())

        sfile = File(open(f'vi_sitemap_{idx}.xml', 'r'))
        os.remove(f'vi_sitemap_{idx}.xml')
        obj = Sitemap.objects.create(
            name = f'vi_sitemap_{idx}.xml',
            sitemap_file = sfile,
        )
        url = obj.get_absolute_url()
        full_url = 'https://vizvasrj.com'+url
        # google = 'https://www.google.com/ping?sitemap='+full_url
        # requests.get(url)
        
