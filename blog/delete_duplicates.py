from django.db.models import Q
from .models import Post
aall = Post.objects.all()[0].id
for rn in range(Post.objects.all()[0].id):
    try:
        instance = Post.objects.get(id=rn)
        print(instance.id)
        print(rn / aall)
    # english_translated_post
        ids = []
        for x in instance.english_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.english_translated_post.all().filter(~Q(id=max(ids))).delete()

    # arabic_translated_post
        ids = []
        for x in instance.arabic_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.arabic_translated_post.all().filter(~Q(id=max(ids))).delete()

    # chinese_translated_post
        ids = []
        for x in instance.chinese_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.chinese_translated_post.all().filter(~Q(id=max(ids))).delete()

    # filipino_translated_post
        ids = []
        for x in instance.filipino_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.filipino_translated_post.all().filter(~Q(id=max(ids))).delete()

    # french_translated_post
        ids = []
        for x in instance.french_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.french_translated_post.all().filter(~Q(id=max(ids))).delete()


    # german_translated_post
        ids = []
        for x in instance.german_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.german_translated_post.all().filter(~Q(id=max(ids))).delete()


    # hindi_translated_post
        ids = []
        for x in instance.hindi_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.hindi_translated_post.all().filter(~Q(id=max(ids))).delete()

    # indonesian_translated_post
        ids = []
        for x in instance.indonesian_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.indonesian_translated_post.all().filter(~Q(id=max(ids))).delete()

    # italian_translated_post
        ids = []
        for x in instance.italian_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.italian_translated_post.all().filter(~Q(id=max(ids))).delete()

    # japanese_translated_post
        ids = []
        for x in instance.japanese_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.japanese_translated_post.all().filter(~Q(id=max(ids))).delete()

    # korean_translated_post
        ids = []
        for x in instance.korean_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.korean_translated_post.all().filter(~Q(id=max(ids))).delete()

    # norwegian_translated_post
        ids = []
        for x in instance.norwegian_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.norwegian_translated_post.all().filter(~Q(id=max(ids))).delete()

    # portuguese_translated_post
        ids = []
        for x in instance.portuguese_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.portuguese_translated_post.all().filter(~Q(id=max(ids))).delete()

    # russian_translated_post
        ids = []
        for x in instance.russian_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.russian_translated_post.all().filter(~Q(id=max(ids))).delete()

    # spanish_translated_post
        ids = []
        for x in instance.spanish_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.spanish_translated_post.all().filter(~Q(id=max(ids))).delete()


    # vietnamese_translated_post
        ids = []
        for x in instance.vietnamese_translated_post.all():
            ids.append(x.id)
        if len(ids) > 1:
            print(max(ids))
            d = instance.vietnamese_translated_post.all().filter(~Q(id=max(ids))).delete()

    except Post.DoesNotExist:
        print(rn, "DOES NOT EXISTS")


