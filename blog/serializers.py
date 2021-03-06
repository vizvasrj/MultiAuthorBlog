
from rest_framework import serializers
from blog.models import (
    Post,
    # Category, 
    Image
)
# from mytag.models import MyCustomTag
from translates.hindi_translate.models import HindiTranslatedPost
from translates.arabic_translate.models import ArabicTranslatedPost
from translates.chinese_translate.models import ChineseTranslatedPost
from translates.filipino_translate.models import FilipinoTranslatedPost
from translates.french_translate.models import FrenchTranslatedPost
from translates.german_translate.models import GermanTranslatedPost
from translates.indonesian_translate.models import IndonesianTranslatedPost
from translates.italian_translate.models import ItalianTranslatedPost
from translates.japanese_translate.models import JapaneseTranslatedPost
from translates.korean_translate.models import KoreanTranslatedPost
from translates.norwegian_translate.models import NorwegianTranslatedPost
from translates.portuguese_translate.models import PortugueseTranslatedPost
from translates.russian_translate.models import RussianTranslatedPost 
from translates.spanish_translate.models import SpanishTranslatedPost
from translates.vietnamese_translate.models import VietnameseTranslatedPost
from translates.english_translate.models import EnglishTranslatedPost
from translates.bengali_translate.models import BengaliTranslatedPost
# from . import views



STATUS_CREATE = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)
class PostSerializer(serializers.Serializer):

    title = serializers.CharField(
        max_length=256
    )
    status = serializers.ChoiceField(
        choices=STATUS_CREATE,
    )
    body = serializers.CharField()
    class Meta:
        model = Post
        fields = (
            'url',
            'author',
            'title',
            'status',
            'body',
        )
    
    # def create(self, validated_data):
    #     pass

    def update(self, validated_data):
        pass

    def validate(self, data):
        title = data['title']
        body = data['body']
        status = data['status']
        validation = {
            'title': title,
            'status': status,
            'body': body,
        }
        return validation


class ENpost(serializers.ModelSerializer):
    class Meta:
        model = EnglishTranslatedPost
        fields = ('id',)


class ARpost(serializers.ModelSerializer):
    class Meta:
        model = ArabicTranslatedPost
        fields = ('id',)


class CNpost(serializers.ModelSerializer):
    class Meta:
        model = ChineseTranslatedPost
        fields = ('id',)


class TApost(serializers.ModelSerializer):
    class Meta:
        model = FilipinoTranslatedPost
        fields = ('id',)


class FRpost(serializers.ModelSerializer):
    class Meta:
        model = FrenchTranslatedPost
        fields = ('id',)


class DEpost(serializers.ModelSerializer):
    class Meta:
        model = GermanTranslatedPost
        fields = ('id',)


class HIpost(serializers.ModelSerializer):
    class Meta:
        model = HindiTranslatedPost
        fields = ('id',)


class IDpost(serializers.ModelSerializer):
    class Meta:
        model = IndonesianTranslatedPost
        fields = ('id',)


class ITpost(serializers.ModelSerializer):
    class Meta:
        model = ItalianTranslatedPost
        fields = ('id',)


class JApost(serializers.ModelSerializer):
    class Meta:
        model = JapaneseTranslatedPost
        fields = ('id',)


class KOpost(serializers.ModelSerializer):
    class Meta:
        model = KoreanTranslatedPost
        fields = ('id',)


class NNpost(serializers.ModelSerializer):
    class Meta:
        model = NorwegianTranslatedPost
        fields = ('id',)


class PTpost(serializers.ModelSerializer):
    class Meta:
        model = PortugueseTranslatedPost
        fields = ('id',)


class RUpost(serializers.ModelSerializer):
    class Meta:
        model = RussianTranslatedPost
        fields = ('id',)


class ESpost(serializers.ModelSerializer):
    class Meta:
        model = SpanishTranslatedPost
        fields = ('id',)


class VIpost(serializers.ModelSerializer):
    class Meta:
        model = VietnameseTranslatedPost
        fields = ('id',)

class BNpost(serializers.ModelSerializer):
    class Meta:
        model = BengaliTranslatedPost
        fields = ('id',)



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'creator_name', 'creator_url', )



class PostCURDSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=256
    )
    body = serializers.CharField()
    status = serializers.ChoiceField(
        choices=STATUS_CREATE
    )
    author = serializers.CharField(
        required=False, read_only=True
    )
    # cover2 = ImageSerializer()
    english_translated_post = ENpost(required=False, many=True, read_only=True)
    arabic_translated_post = ARpost(required=False, many=True, read_only=True)
    chinese_translated_post = CNpost(required=False, many=True, read_only=True)
    filipino_translated_post = TApost(required=False, many=True, read_only=True)
    french_translated_post = FRpost(required=False, many=True, read_only=True)
    german_translated_post = DEpost(required=False, many=True, read_only=True)
    hindi_translated_post = HIpost(required=False, many=True, read_only=True)
    indonesian_translated_post = IDpost(required=False, many=True, read_only=True)
    italian_translated_post = ITpost(required=False, many=True, read_only=True)
    japanese_translated_post = JApost(required=False, many=True, read_only=True)
    korean_translated_post = KOpost(required=False, many=True, read_only=True)
    norwegian_translated_post = NNpost(required=False, many=True, read_only=True)
    portuguese_translated_post = PTpost(required=False, many=True, read_only=True)
    russian_translated_post = RUpost(required=False, many=True, read_only=True)
    spanish_translated_post = ESpost(required=False, many=True, read_only=True)
    vietnamese_translated_post = VIpost(required=False, many=True, read_only=True)
    bengali_translated_post = BNpost(required=False, many=True, read_only=True)
    t = serializers.CharField(
        max_length=20,
        allow_null=True,
        required=False,
    )
    scrape_url = serializers.CharField(read_only=True)
    class Meta:
        model = Post
        fields = (
            'id', 
            'title', 
            'body', 
            'status', 
            'author', 
            'cover2',
            'english_translated_post',
            'arabic_translated_post',
            'chinese_translated_post',
            'filipino_translated_post',
            'french_translated_post',
            'german_translated_post',
            'hindi_translated_post',
            'indonesian_translated_post',
            'italian_translated_post',
            'japanese_translated_post',
            'korean_translated_post',
            'norwegian_translated_post',
            'portuguese_translated_post',
            'russian_translated_post',
            'spanish_translated_post',
            'vietnamese_translated_post',
            'bengali_translated_post',
            't',
            'scrape_url',
            )


class PostListSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=256
    )
    body = serializers.CharField()
    status = serializers.ChoiceField(
        choices=STATUS_CREATE
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'status',)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class ENpost(serializers.ModelSerializer):
    class Meta:
        model = EnglishTranslatedPost
        fields = ('id', 'meta_description')


class ARpost(serializers.ModelSerializer):
    class Meta:
        model = ArabicTranslatedPost
        fields = ('id', 'meta_description')


class CNpost(serializers.ModelSerializer):
    class Meta:
        model = ChineseTranslatedPost
        fields = ('id', 'meta_description')


class TApost(serializers.ModelSerializer):
    class Meta:
        model = FilipinoTranslatedPost
        fields = ('id', 'meta_description')


class FRpost(serializers.ModelSerializer):
    class Meta:
        model = FrenchTranslatedPost
        fields = ('id', 'meta_description')


class DEpost(serializers.ModelSerializer):
    class Meta:
        model = GermanTranslatedPost
        fields = ('id', 'meta_description')


class HIpost(serializers.ModelSerializer):
    class Meta:
        model = HindiTranslatedPost
        fields = ('id', 'meta_description')


class IDpost(serializers.ModelSerializer):
    class Meta:
        model = IndonesianTranslatedPost
        fields = ('id', 'meta_description')


class ITpost(serializers.ModelSerializer):
    class Meta:
        model = ItalianTranslatedPost
        fields = ('id', 'meta_description')


class JApost(serializers.ModelSerializer):
    class Meta:
        model = JapaneseTranslatedPost
        fields = ('id', 'meta_description')


class KOpost(serializers.ModelSerializer):
    class Meta:
        model = KoreanTranslatedPost
        fields = ('id', 'meta_description')


class NNpost(serializers.ModelSerializer):
    class Meta:
        model = NorwegianTranslatedPost
        fields = ('id', 'meta_description')


class PTpost(serializers.ModelSerializer):
    class Meta:
        model = PortugueseTranslatedPost
        fields = ('id', 'meta_description')


class RUpost(serializers.ModelSerializer):
    class Meta:
        model = RussianTranslatedPost
        fields = ('id', 'meta_description')


class ESpost(serializers.ModelSerializer):
    class Meta:
        model = SpanishTranslatedPost
        fields = ('id', 'meta_description')


class VIaudio(serializers.ModelSerializer):
    class Meta:
        model = VietnameseTranslatedPost
        fields = ('id', 'meta_description')

class BNaudio(serializers.ModelSerializer):
    class Meta:
        model = BengaliTranslatedPost
        fields = ('id', 'meta_description')

class OnlyAudioShow(serializers.ModelSerializer):
    # title = serializers.CharField(
    #     max_length=256, read_only=True
    # )
    # body = serializers.CharField(read_only=True)
    english_translated_post = ENpost(required=False, many=True, read_only=True)
    arabic_translated_post = ARpost(required=False, many=True, read_only=True)
    chinese_translated_post = CNpost(required=False, many=True, read_only=True)
    filipino_translated_post = TApost(required=False, many=True, read_only=True)
    french_translated_post = FRpost(required=False, many=True, read_only=True)
    german_translated_post = DEpost(required=False, many=True, read_only=True)
    hindi_translated_post = HIpost(required=False, many=True, read_only=True)
    indonesian_translated_post = IDpost(required=False, many=True, read_only=True)
    italian_translated_post = ITpost(required=False, many=True, read_only=True)
    japanese_translated_post = JApost(required=False, many=True, read_only=True)
    korean_translated_post = KOpost(required=False, many=True, read_only=True)
    norwegian_translated_post = NNpost(required=False, many=True, read_only=True)
    portuguese_translated_post = PTpost(required=False, many=True, read_only=True)
    russian_translated_post = RUpost(required=False, many=True, read_only=True)
    spanish_translated_post = ESpost(required=False, many=True, read_only=True)

    vietnamese_translated_post = VIaudio(required=False, many=True, read_only=True)
    bengali_translated_post = BNpost(required=False, many=True, read_only=True)
    t = serializers.CharField(
        max_length=20,
        allow_null=True,
        required=False,
    )
    class Meta:
        model = Post
        fields = (
            'id', 
            # 'title', 
            # 'body', 
            'english_translated_post',
            'arabic_translated_post',
            'chinese_translated_post',
            'filipino_translated_post',
            'french_translated_post',
            'german_translated_post',
            'hindi_translated_post',
            'indonesian_translated_post',
            'italian_translated_post',
            'japanese_translated_post',
            'korean_translated_post',
            'norwegian_translated_post',
            'portuguese_translated_post',
            'russian_translated_post',
            'spanish_translated_post',
            'vietnamese_translated_post',
            'bengali_translated_post',
            't',
            )

class SourcePostSerializer(serializers.Serializer):
    text = serializers.CharField()

    
class ENpostall(serializers.ModelSerializer):
    class Meta:
        model = EnglishTranslatedPost
        fields = ('title', 'body',)


class OnlyEngShow(serializers.ModelSerializer):
    english_translated_post = ENpostall(required=False, many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'english_translated_post')
