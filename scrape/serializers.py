from .models import HealthlineParsed, Healthline
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post


class HLPSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()
    
    class Meta:
        model = HealthlineParsed
        fields = (
            'title',
            'description',
            'url',
        )


class UntranslatedSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = Healthline
        fields = (
            'id',
            'title',
            'description',
            'url'
        )