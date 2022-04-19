def bn_t(tag=None, post=None):
    from translates.bengali_translate.models import BengaliTranslatedTag
    if tag:
        # this will return single tag
        return BengaliTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if BengaliTranslatedTag.objects.filter(tag__post=post.id).exists():
            return BengaliTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()
    


def bn_p(post=None):
    from translates.bengali_translate.models import BengaliTranslatedPost
    if post:
        return BengaliTranslatedPost.objects.filter(post=post).latest()
