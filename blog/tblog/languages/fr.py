def fr_t(tag=None, post=None):
    from translates.french_translate.models import FrenchTranslatedTag
    if tag:
        # this will return single tag
        return FrenchTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if FrenchTranslatedTag.objects.filter(tag__post=post.id).exists():
            return FrenchTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def fr_p(post=None):
    from translates.french_translate.models import FrenchTranslatedPost
    if post:
        return FrenchTranslatedPost.objects.filter(post=post).latest()
