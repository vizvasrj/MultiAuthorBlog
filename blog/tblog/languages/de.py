def de_t(tag=None, post=None):
    from translates.german_translate.models import GermanTranslatedTag
    if tag:
        # this will return single tag
        return GermanTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return GermanTranslatedTag.objects.filter(tag__post=post.id)


def de_p(post=None):
    from translates.german_translate.models import GermanTranslatedPost
    if post:
        return GermanTranslatedPost.objects.filter(post=post).latest()
