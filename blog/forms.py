# core
from django import forms

# local
from .models import Post, Comment

# 3rd party
from trumbowyg.widgets import TrumbowygWidget
from taggit.forms import TagWidget
from mptt.forms import TreeNodeChoiceField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'body', 'tags', 'cover'
        )

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control myfieldclass'}
            ),
            'body': TrumbowygWidget(
                attrs={
                    'class': 'form-control myfieldclass',
                }
            ),
            'tags': TagWidget(
                attrs={
                    'class': 'form-control myfieldclass',
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'form-control myfieldclass',
                    'required': False
                }
            )
        }


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Comment.objects.all()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('parent', 'body')
        widgets = {
            'body': forms.Textarea()
        }

    