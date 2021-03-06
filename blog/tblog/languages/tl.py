def tl_t(tag=None, post=None):
    from translates.filipino_translate.models import FilipinoTranslatedTag
    if tag:
        # this will return single tag
        return FilipinoTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if FilipinoTranslatedTag.objects.filter(tag__post=post.id).exists():
            return FilipinoTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def tl_p(post=None):
    from translates.filipino_translate.models import FilipinoTranslatedPost
    if post:
        return FilipinoTranslatedPost.objects.filter(post=post).latest()
