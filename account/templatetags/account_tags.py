from django import template
from blog.models import Post

from django.db.models import Count
from account.models import Profile

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(is_safe=True, name='single_tag')
def single_tag(tag, ln):

    if ln == 'ar':
        from translates.arabic_translate.models import ArabicTranslatedTag
        t_tag = ArabicTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'hi':
        from translates.hindi_translate.models import HindiTranslatedTag
        t_tag = HindiTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'zh-hans':
        from translates.chinese_translate.models import ChineseTranslatedTag
        t_tag = ChineseTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'id':
        from translates.indonesian_translate.models import IndonesianTranslatedTag
        t_tag = IndonesianTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'it':
        from translates.italian_translate.models import ItalianTranslatedTag
        t_tag = ItalianTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'ja':
        from translates.japanese_translate.models import JapaneseTranslatedTag
        t_tag = JapaneseTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'ko':
        from translates.korean_translate.models import KoreanTranslatedTag
        t_tag = KoreanTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'nn':
        from translates.norwegian_translate.models import NorwegianTranslatedTag
        t_tag = NorwegianTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'pt':
        from translates.portuguese_translate.models import PortugueseTranslatedTag
        t_tag = PortugueseTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'ru':
        from translates.russian_translate.models import RussianTranslatedTag
        t_tag = RussianTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'es':
        from translates.spanish_translate.models import SpanishTranslatedTag
        t_tag = SpanishTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'en':
        from translates.english_translate.models import EnglishTranslatedTag
        t_tag = EnglishTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'tl':
        from translates.filipino_translate.models import FilipinoTranslatedTag
        t_tag = FilipinoTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'fr':
        from translates.french_translate.models import FrenchTranslatedTag
        t_tag = FrenchTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'de':
        from translates.german_translate.models import GermanTranslatedTag
        t_tag = GermanTranslatedTag.objects.get(tag=tag)
    
    elif ln == 'vi':
        from translates.vietnamese_translate.models import VietnameseTranslatedTag
        t_tag = VietnameseTranslatedTag.objects.get(tag=tag)

    else:
        t_tag = tag
    return t_tag