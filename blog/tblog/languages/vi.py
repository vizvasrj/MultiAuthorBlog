def vi_t(tag=None, post=None):
    from translates.vietnamese_translate.models import VietnameseTranslatedTag
    if tag:
        # this will return single tag
        return VietnameseTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if VietnameseTranslatedTag.objects.filter(tag__post=post.id).exists():
            return VietnameseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def vi_p(post=None):
    from translates.vietnamese_translate.models import VietnameseTranslatedPost
    if post:
        return VietnameseTranslatedPost.objects.filter(post=post).latest()
