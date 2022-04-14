def pt_t(tag=None, post=None):
    from translates.portuguese_translate.models import PortugueseTranslatedTag
    if tag:
        # this will return single tag
        return PortugueseTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return PortugueseTranslatedTag.objects.filter(tag__post=post.id)


def pt_p(post=None):
    from translates.portuguese_translate.models import PortugueseTranslatedPost
    if post:
        return PortugueseTranslatedPost.objects.filter(post=post).latest()
