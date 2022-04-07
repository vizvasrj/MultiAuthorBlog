from translates.hindi_translate.models import HindiTranslatedTag
from translates.arabic_translate.models import ArabicTranslatedTag
from translates.chinese_translate.models import ChineseTranslatedTag
from translates.filipino_translate.models import FilipinoTranslatedTag
from translates.french_translate.models import FrenchTranslatedTag
from translates.german_translate.models import GermanTranslatedTag
from translates.indonesian_translate.models import IndonesianTranslatedTag
from translates.italian_translate.models import ItalianTranslatedTag
from translates.japanese_translate.models import JapaneseTranslatedTag
from translates.korean_translate.models import KoreanTranslatedTag
from translates.norwegian_translate.models import NorwegianTranslatedTag
from translates.portuguese_translate.models import PortugueseTranslatedTag
from translates.russian_translate.models import RussianTranslatedTag 
from translates.spanish_translate.models import SpanishTranslatedTag
from translates.vietnamese_translate.models import VietnameseTranslatedTag
from translates.english_translate.models import EnglishTranslatedTag

from mytag.models import MyCustomTag

from django.core.exceptions import ObjectDoesNotExist

def language_in_post_detail(post, language):
    try:
        if language == 'en':
            if post.english_translated_post.latest():
                return post.english_translated_post.latest()
            else:
                return post

        elif language == 'zh-hans':
            if post.chinese_translated_post.latest():
                return post.chinese_translated_post.latest()
            else:
                return post

        elif language == 'hi':
            if post.hindi_translated_post.latest():
                return post.hindi_translated_post.latest()
            else:
                return post
            
        elif language == 'ar':
            if post.arabic_translated_post.latest():
                return post.arabic_translated_post.latest()
            else:
                return post

        elif language == 'tl':
            if post.filipino_translated_post.latest():
                return post.filipino_translated_post.latest()
            else:
                return post

        elif language == 'fr':
            if post.french_translated_post.latest():
                return post.french_translated_post.latest()
            else:
                return post
        
        elif language == 'de':
            if post.german_translated_post.latest():
                return post.german_translated_post.latest()
            else:
                return post
        
        elif language == 'id':
            if post.indonesian_translated_post.latest():
                return post.indonesian_translated_post.latest()
            else:
                return post
        
        elif language == 'it':
            if post.italian_translated_post.latest():
                return post.italian_translated_post.latest()
            else:
                return post

        elif language == 'ja':
            if post.japanese_translated_post.latest():
                return post.japanese_translated_post.latest()
            else:
                return post
        
        elif language == 'ko':
            if post.korean_translated_post.latest():
                return post.korean_translated_post.latest()
            else:
                return post
        
        elif language == 'nn':
            if post.norwegian_translated_post.latest():
                return post.norwegian_translated_post.latest()
            else:
                return post

        elif language == 'pt':
            if post.portuguese_translated_post.latest():
                return post.portuguese_translated_post.latest()
            else:
                return post

        elif language == 'ru':
            if post.russian_translated_post.latest():
                return post.russian_translated_post.latest()
            else:
                return post
        
        elif language == 'es':
            if post.spanish_translated_post.latest():
                return post.spanish_translated_post.latest()
            else:
                return post
        
        elif language == 'vi':
            if post.vietnamese_translated_post.latest():
                return post.vietnamese_translated_post.latest()
            else:
                return post
        # I know it will never get inside this else statement
        else:
            # print('inside else')
            return post
    except ObjectDoesNotExist:
        return post

def language_in_post_tags(post, language):
    default = MyCustomTag.objects.filter(post=post.id)
    if language == 'en':
        if EnglishTranslatedTag.objects.filter(tag__post=post.id):
            return EnglishTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'zh-hans':
        if ChineseTranslatedTag.objects.filter(tag__post=post.id):
            return ChineseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'hi':
        if HindiTranslatedTag.objects.filter(tag__post=post.id):
            return HindiTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
        
    elif language == 'ar':
        if ArabicTranslatedTag.objects.filter(tag__post=post.id):
            return ArabicTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'tl':
        if FilipinoTranslatedTag.objects.filter(tag__post=post.id):
            return FilipinoTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'fr':
        if FrenchTranslatedTag.objects.filter(tag__post=post.id):
            return FrenchTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'de':
        if GermanTranslatedTag.objects.filter(tag__post=post.id):
            return GermanTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'id':
        if IndonesianTranslatedTag.objects.filter(tag__post=post.id):
            return IndonesianTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'it':
        if ItalianTranslatedTag.objects.filter(tag__post=post.id):
            return ItalianTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'ja':
        if JapaneseTranslatedTag.objects.filter(tag__post=post.id):
            return JapaneseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'ko':
        if KoreanTranslatedTag.objects.filter(tag__post=post.id):
            return KoreanTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'nn':
        if NorwegianTranslatedTag.objects.filter(tag__post=post.id):
            return NorwegianTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'pt':
        if PortugueseTranslatedTag.objects.filter(tag__post=post.id):
            return PortugueseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default

    elif language == 'ru':
        if RussianTranslatedTag.objects.filter(tag__post=post.id):
            return RussianTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'es':
        if SpanishTranslatedTag.objects.filter(tag__post=post.id):
            return SpanishTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    
    elif language == 'vi':
        if VietnameseTranslatedTag.objects.filter(tag__post=post.id):
            return VietnameseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return default
    # I know it will never get inside this else statement
    else:
        # print('inside else')
        return default


