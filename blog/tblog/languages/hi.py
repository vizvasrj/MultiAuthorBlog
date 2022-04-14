def hi_t(tag=None, post=None):
    from translates.hindi_translate.models import HindiTranslatedTag
    if tag:
        # this will return single tag
        return HindiTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return HindiTranslatedTag.objects.filter(tag__post=post.id)


def hi_p(post=None):
    from translates.hindi_translate.models import HindiTranslatedPost
    if post:
        return HindiTranslatedPost.objects.filter(post=post).latest()
