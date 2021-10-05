
from django import forms
from django.forms import widgets

from .models import Publication

from taggit_autosuggest.widgets import TagAutoSuggest
from django_select2 import forms as s2forms



class CoAuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["username__istartswith", "email__icontains"]


class PubForm(forms.ModelForm):
    
    class Meta:
        model = Publication
        fields = ('name', 'tags', 'image', 'content_creater', 'about')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'myfieldclass border padding-15 border-bottom', 'autocomplete': 'off',
                'placeholder': 'Name'}
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': 'Tags',
                    'required': False,
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': ' border btn myfieldclass',
                    'required': False
                }
            ),
            'about': forms.Textarea(
                # config={'minHeight': 100}
                attrs={
                'placeholder': 'What\'s your Publication about of.',
                    'class': 'myfieldclass padding-15',
                }
            ),
            'content_creater': CoAuthorsWidget(
                attrs={
                    'class': '',
                    'style': 'width: 100%',
                }
            ),
        }


class ManageForm(forms.ModelForm):
    
    class Meta:
        model = Publication
        fields = ('name', 'tags', 'image', 'content_creater', 'about')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'myfieldclass border padding-15 border-bottom', 'autocomplete': 'off',
                'placeholder': 'Name'}
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': 'Tags',
                    'required': False,
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': ' border btn myfieldclass',
                    'required': False
                }
            ),
            'about': forms.Textarea(
                # config={'minHeight': 100}
                attrs={
                'placeholder': 'What\'s your Publication about of.',
                    'class': 'myfieldclass padding-15',
                }
            ),
            'content_creater': CoAuthorsWidget(
                attrs={
                    'class': '',
                    'style': 'width: 100%',
                }
            ),
        }
