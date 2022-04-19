def ja_t(tag=None, post=None):
    from translates.japanese_translate.models import JapaneseTranslatedTag
    if tag:
        # this will return single tag
        return JapaneseTranslatedTag.objects.get(tag=tag)
    elif post:
        # this will return multiple tags
        if JapaneseTranslatedTag.objects.filter(tag__post=post.id).exists():
            return JapaneseTranslatedTag.objects.filter(tag__post=post.id)
        else:
            return post.tags.all()


def ja_p(post=None):
    from translates.japanese_translate.models import JapaneseTranslatedPost
    if post:
        return JapaneseTranslatedPost.objects.filter(post=post).latest()
