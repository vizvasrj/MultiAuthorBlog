def it_t(tag=None, post=None):
    from translates.italian_translate.models import ItalianTranslatedTag
    if tag:
        # this will return single tag
        return ItalianTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if ItalianTranslatedTag.objects.filter(tag__post=post.id).exists():
            return ItalianTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def it_p(post=None):
    from translates.italian_translate.models import ItalianTranslatedPost
    if post:
        return ItalianTranslatedPost.objects.filter(post=post).latest()
