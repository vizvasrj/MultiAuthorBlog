# core
from django import forms

# local
from .models import Post, Comment

# 3rd party
from trumbowyg.widgets import TrumbowygWidget
from taggit.forms import TagWidget
from mptt.forms import TreeNodeChoiceField
from bootstrap_datepicker_plus import DatePickerInput


class PostForm(forms.ModelForm):
    # publish = forms.DateField(
    #     widget=DatePickerInput(format='%m/%d/%Y')
    # )

    class Meta:
        model = Post
        fields = (
            'title', 'body', 'tags', 'cover'
        )

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'myfieldclass '}
            ),
            'body': TrumbowygWidget(
                attrs={
                    'class': 'myfieldclass ',
                }
            ),
            'tags': TagWidget(
                attrs={
                    'class': 'myfieldclass',
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'myfieldclass',
                    'required': False
                }
            ),
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
