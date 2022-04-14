def en_t(tag=None, post=None):
    from translates.english_translate.models import EnglishTranslatedTag
    if tag:
        # this will return single tag
        return EnglishTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return EnglishTranslatedTag.objects.filter(tag__post=post.id)


def en_p(post=None):
    from translates.english_translate.models import EnglishTranslatedPost
    if post:
        return EnglishTranslatedPost.objects.filter(post=post).latest()
