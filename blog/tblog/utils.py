from django.core.exceptions import ObjectDoesNotExist

def language_in_post_tags(post, language, n=3):
    from mytag.models import MyCustomTag
    default = MyCustomTag.objects.filter(post=post.id)
    if language == 'en':
        from translates.english_translate.models import EnglishTranslatedTag
        if EnglishTranslatedTag.objects.filter(tag__post=post.id):
            return EnglishTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'zh-hans':
        from translates.chinese_translate.models import ChineseTranslatedTag
        if ChineseTranslatedTag.objects.filter(tag__post=post.id):
            return ChineseTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'hi':
        from translates.hindi_translate.models import HindiTranslatedTag
        if HindiTranslatedTag.objects.filter(tag__post=post.id):
            return HindiTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
        
    elif language == 'ar':
        from translates.arabic_translate.models import ArabicTranslatedTag
        if ArabicTranslatedTag.objects.filter(tag__post=post.id):
            return ArabicTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'tl':
        from translates.filipino_translate.models import FilipinoTranslatedTag
        if FilipinoTranslatedTag.objects.filter(tag__post=post.id):
            return FilipinoTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'fr':
        from translates.french_translate.models import FrenchTranslatedTag
        if FrenchTranslatedTag.objects.filter(tag__post=post.id):
            return FrenchTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'de':
        from translates.german_translate.models import GermanTranslatedTag
        if GermanTranslatedTag.objects.filter(tag__post=post.id):
            return GermanTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'id':
        from translates.indonesian_translate.models import IndonesianTranslatedTag
        if IndonesianTranslatedTag.objects.filter(tag__post=post.id):
            return IndonesianTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'it':
        from translates.italian_translate.models import ItalianTranslatedTag
        if ItalianTranslatedTag.objects.filter(tag__post=post.id):
            return ItalianTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'ja':
        from translates.japanese_translate.models import JapaneseTranslatedTag
        if JapaneseTranslatedTag.objects.filter(tag__post=post.id):
            return JapaneseTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'ko':
        from translates.korean_translate.models import KoreanTranslatedTag
        if KoreanTranslatedTag.objects.filter(tag__post=post.id):
            return KoreanTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'nn':
        from translates.norwegian_translate.models import NorwegianTranslatedTag
        if NorwegianTranslatedTag.objects.filter(tag__post=post.id):
            return NorwegianTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'pt':
        from translates.portuguese_translate.models import PortugueseTranslatedTag
        if PortugueseTranslatedTag.objects.filter(tag__post=post.id):
            return PortugueseTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default

    elif language == 'ru':
        from translates.russian_translate.models import RussianTranslatedTag
        if RussianTranslatedTag.objects.filter(tag__post=post.id):
            return RussianTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'es':
        from translates.spanish_translate.models import SpanishTranslatedTag
        if SpanishTranslatedTag.objects.filter(tag__post=post.id):
            return SpanishTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    
    elif language == 'vi':
        from translates.vietnamese_translate.models import VietnameseTranslatedTag
        if VietnameseTranslatedTag.objects.filter(tag__post=post.id):
            return VietnameseTranslatedTag.objects.filter(tag__post=post.id)[:n]
        else:
            return default
    # I know it will never get inside this else statement
    else:
        # print('inside else')
        return default



# This function is used to get post or tags to given language 
# is_ represent which type of data is coming is it tag, or post
# need_ represent what data do you need translated_tags or translated_post

def get_tpost_ttags(is_post=None, is_tag=None, need_tags=None, need_post=None  ,tag=None, post=None, language=None, n=3):
    try:
        if language == 'en':
            if is_tag:
                from blog.tblog.languages.en import en_t
                # need translate tag of given translate tag
                return en_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.en import en_t
                    # return multiple translated tags of given un translated post
                    return en_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.en import en_p
                    return en_p(post=is_post)


        if language == 'zh-hans':
            if is_tag:
                from blog.tblog.languages.zh_hans import zh_hans_t
                # need translate tag of given translate tag
                return zh_hans_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.zh_hans import zh_hans_t
                    # return multiple translated tags of givzh_hans un translated post
                    return zh_hans_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.zh_hans import zh_hans_p
                    return zh_hans_p(post=is_post)


        if language == 'hi':
            if is_tag:
                from blog.tblog.languages.hi import hi_t
                # need translate tag of given translate tag
                return hi_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.hi import hi_t
                    # return multiple translated tags of givhi un translated post
                    return hi_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.hi import hi_p
                    return hi_p(post=is_post)
            
        if language == 'ar':
            if is_tag:
                from blog.tblog.languages.ar import ar_t
                # need translate tag of given translate tag
                return ar_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.ar import ar_t
                    # return multiple translated tags of given un translated post
                    return ar_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.ar import ar_p
                    return ar_p(post=is_post)

        if language == 'tl':
            if is_tag:
                from blog.tblog.languages.tl import tl_t
                # need translate tag of given translate tag
                return tl_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.tl import tl_t
                    # return multiple translated tags of given un translated post
                    return tl_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.tl import tl_p
                    return tl_p(post=is_post)

        if language == 'fr':
            if is_tag:
                from blog.tblog.languages.fr import fr_t
                # need translate tag of given translate tag
                return fr_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.fr import fr_t
                    # return multiple translated tags of given un translated post
                    return fr_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.fr import fr_p
                    return fr_p(post=is_post)
        
        if language == 'de':
            if is_tag:
                from blog.tblog.languages.de import de_t
                # need translate tag of given translate tag
                return de_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.de import de_t
                    # return multiple translated tags of given un translated post
                    return de_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.de import de_p
                    return de_p(post=is_post)
        
        if language == 'id':
            if is_tag:
                from blog.tblog.languages.id import id_t
                # need translate tag of given translate tag
                return id_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.id import id_t
                    # return multiple translated tags of given un translated post
                    return id_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.id import id_p
                    return id_p(post=is_post)
        
        if language == 'it':
            if is_tag:
                from blog.tblog.languages.it import it_t
                # need translate tag of given translate tag
                return it_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.it import it_t
                    # return multiple translated tags of given un translated post
                    return it_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.it import it_p
                    return it_p(post=is_post)

        if language == 'ja':
            if is_tag:
                from blog.tblog.languages.ja import ja_t
                # need translate tag of given translate tag
                return ja_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.ja import ja_t

                    # return multiple translated tags of given un translated post
                    return ja_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.ja import ja_p
                    return ja_p(post=is_post)
        
        if language == 'ko':
            if is_tag:
                from blog.tblog.languages.ko import ko_t
                # need translate tag of given translate tag
                return ko_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.ko import ko_t
                    # return multiple translated tags of given un translated post
                    return ko_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.ko import ko_p
                    return ko_p(post=is_post)
        
        if language == 'nn':
            if is_tag:
                from blog.tblog.languages.nn import nn_t
                # need translate tag of given translate tag
                return nn_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.nn import nn_t
                    # return multiple translated tags of given un translated post
                    return nn_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.nn import nn_p
                    return nn_p(post=is_post)

        if language == 'pt':
            if is_tag:
                from blog.tblog.languages.pt import pt_t
                # need translate tag of given translate tag
                return pt_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.pt import pt_t
                    # return multiple translated tags of given un translated post
                    return pt_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.pt import pt_p
                    return pt_p(post=is_post)

        if language == 'ru':
            if is_tag:
                from blog.tblog.languages.ru import ru_t
                # need translate tag of given translate tag
                return ru_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.ru import ru_t
                    # return multiple translated tags of given un translated post
                    return ru_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.ru import ru_p
                    return ru_p(post=is_post)
        
        if language == 'es':
            if is_tag:
                from blog.tblog.languages.es import es_t
                # need translate tag of given translate tag
                return es_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.es import es_t
                    # return multiple translated tags of given un translated post
                    return es_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.es import es_p
                    return es_p(post=is_post)
        
        if language == 'vi':
            if is_tag:
                from blog.tblog.languages.vi import vi_t
                # need translate tag of given translate tag
                return vi_t(tag=tag)
            elif is_post:
                if need_tags:
                    from blog.tblog.languages.vi import vi_t
                    # return multiple translated tags of given un translated post
                    return vi_t(post=is_post)
                elif need_post:
                    from blog.tblog.languages.vi import vi_p
                    return vi_p(post=is_post)
    # I know it will never get inside this else statement
    except ObjectDoesNotExist:
        # print('inside else')
        return is_post


