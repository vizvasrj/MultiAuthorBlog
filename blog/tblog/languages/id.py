def id_t(tag=None, post=None):
    from translates.indonesian_translate.models import IndonesianTranslatedTag
    if tag:
        # this will return single tag
        return IndonesianTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if IndonesianTranslatedTag.objects.filter(tag__post=post.id).exists():
            return IndonesianTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def id_p(post=None):
    from translates.indonesian_translate.models import IndonesianTranslatedPost
    if post:
        return IndonesianTranslatedPost.objects.filter(post=post).latest()
