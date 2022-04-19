def ar_t(tag=None, post=None):
    from translates.arabic_translate.models import ArabicTranslatedTag
    if tag:
        # this will return single tag
        return ArabicTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if ArabicTranslatedTag.objects.filter(tag__post=post.id).exists():
            return ArabicTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def ar_p(post=None):
    from translates.arabic_translate.models import ArabicTranslatedPost
    if post:
        return ArabicTranslatedPost.objects.filter(post=post).latest()
