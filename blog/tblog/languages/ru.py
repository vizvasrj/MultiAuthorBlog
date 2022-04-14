def ru_t(tag=None, post=None):
    from translates.russian_translate.models import RussianTranslatedTag
    if tag:
        # this will return single tag
        return RussianTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return RussianTranslatedTag.objects.filter(tag__post=post.id)


def ru_p(post=None):
    from translates.russian_translate.models import RussianTranslatedPost
    if post:
        return RussianTranslatedPost.objects.filter(post=post).latest()
