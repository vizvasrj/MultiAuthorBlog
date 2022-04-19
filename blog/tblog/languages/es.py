def es_t(tag=None, post=None):
    from translates.spanish_translate.models import SpanishTranslatedTag
    if tag:
        # this will return single tag
        return SpanishTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if SpanishTranslatedTag.objects.filter(tag__post=post.id).exists():
            return SpanishTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def es_p(post=None):
    from translates.spanish_translate.models import SpanishTranslatedPost
    if post:
        return SpanishTranslatedPost.objects.filter(post=post).latest()
