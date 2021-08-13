# core
from typing_extensions import Required
from django import forms
from django.forms import widgets

# local
from .models import Post

# 3rd party
from trumbowyg.widgets import TrumbowygWidget
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'category', 'body', 'tags', 'cover'
        )

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'category': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'body': TrumbowygWidget(),
            'tags': TagWidget(),
            'cover': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'required': False
                }
            )
        }