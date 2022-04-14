def nn_t(tag=None, post=None):
    from translates.norwegian_translate.models import NorwegianTranslatedTag
    if tag:
        # this will return single tag
        return NorwegianTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return NorwegianTranslatedTag.objects.filter(tag__post=post.id)


def nn_p(post=None):
    from translates.norwegian_translate.models import NorwegianTranslatedPost
    if post:
        return NorwegianTranslatedPost.objects.filter(post=post).latest()
