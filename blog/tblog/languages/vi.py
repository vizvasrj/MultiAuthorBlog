def vi_t(tag=None, post=None):
    from translates.vietnamese_translate.models import VietnameseTranslatedTag
    if tag:
        # this will return single tag
        return VietnameseTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        return VietnameseTranslatedTag.objects.filter(tag__post=post.id)


def vi_p(post=None):
    from translates.vietnamese_translate.models import VietnameseTranslatedPost
    if post:
        return VietnameseTranslatedPost.objects.filter(post=post).latest()
