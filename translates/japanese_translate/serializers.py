from .models import JapaneseTranslatedPost
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:

        model = Post
        fields = (
            'id',
            # 'title',
        )


class JTPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    body = serializers.CharField()
    post = PostSerializer()
    edited_by = UsersSerializer(
         many=True, read_only=True,
    )
    class Meta:
        model = JapaneseTranslatedPost
        fields = ('id', 'post', 'title', 'body', 'edited_by')