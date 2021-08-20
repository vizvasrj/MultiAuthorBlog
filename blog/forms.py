# core
from django import forms

# local
from .models import Post, Comment

# 3rd party
from taggit.forms import TagWidget
from mptt.forms import TreeNodeChoiceField
from django_editorjs_fields import EditorJsWidget
from django_ckeditor_5.widgets import CKEditor5Widget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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
                attrs={'class': 'myfieldclass', 'autocomplete': 'off'}
            ),
            'body': CKEditor5Widget(

                # config={'minHeight': 100}
                # attrs={
                #     'class': 'myfieldclass ',
                # }
            ),
            'tags': TagWidget(
                attrs={
                    'class': 'myfieldclass'
                    , 'autocomplete': 'off'
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
    body = forms.TextInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        self.fields['body'].required = False

    class Meta:
        model = Comment
        fields = ('parent', 'body')
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'myfieldclass',
                }
            )
        }


class SearchForm(forms.Form):
    query = forms.CharField()