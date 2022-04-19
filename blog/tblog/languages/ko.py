def ko_t(tag=None, post=None):
    from translates.korean_translate.models import KoreanTranslatedTag
    if tag:
        # this will return single tag
        return KoreanTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if KoreanTranslatedTag.objects.filter(tag__post=post.id).exists():
            return KoreanTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def ko_p(post=None):
    from translates.korean_translate.models import KoreanTranslatedPost
    if post:
        return KoreanTranslatedPost.objects.filter(post=post).latest()
