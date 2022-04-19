def zh_hans_t(tag=None, post=None):
    from translates.chinese_translate.models import ChineseTranslatedTag
    if tag:
        # this will return single tag
        return ChineseTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if ChineseTranslatedTag.objects.filter(tag__post=post.id).exists():
            return ChineseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def zh_hans_p(post=None):
    from translates.chinese_translate.models import ChineseTranslatedPost
    if post:
        return ChineseTranslatedPost.objects.filter(post=post).latest()
