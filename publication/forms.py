
from django import forms
from django.forms import widgets

from blog.forms import PostForm

from .models import Publication

from taggit_autosuggest.widgets import TagAutoSuggest
from django_select2 import forms as s2forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class CoAuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["username__istartswith", "email__icontains"]


class PubForm(forms.ModelForm):

    writer = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=s2forms.ModelSelect2MultipleWidget(
            # model=User,
            search_fields = ["username__istartswith", "email__icontains"]
        )
    )    

    def __init__(self, user, *args, **kwargs):
        super(PubForm, self).__init__(*args, **kwargs)
        # if user != None:
        self.fields['writer'].queryset = User.objects.exclude(id=user.id)

    
    class Meta:
        model = Publication
        fields = ('name', 'tags', 'image', 'writer', 'about')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'myfieldclass border padding-15 border-bottom', 'autocomplete': 'off',
                'placeholder': _('Name')}
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': _('Tags'),
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
                'placeholder': _("What's your Publication about of."),
                    'class': 'myfieldclass padding-15',
                }
            ),
            # 'writer': CoAuthorsWidget(
            #     attrs={
            #         'class': '',
            #         'style': 'width: 100%',
            #     }
            # ),
        }


class ManageForm(forms.ModelForm):

    writer = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=s2forms.ModelSelect2MultipleWidget(
            # model=User,
            search_fields = ["username__istartswith", "email__icontains"]
        )
    )    

    def __init__(self, user, *args, **kwargs):
        super(ManageForm, self).__init__(*args, **kwargs)
        # if user != None:
        self.fields['writer'].queryset = User.objects.exclude(id=user.id)
    
    class Meta:
        model = Publication
        fields = ('name', 'tags', 'image', 'writer', 'about')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'myfieldclass border padding-15 border-bottom', 'autocomplete': 'off',
                'placeholder': _('Name')}
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': _('Tags'),
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
                'placeholder': _("What's your Publication about of."),
                    'class': 'myfieldclass padding-15',
                }
            ),
            # 'writer': CoAuthorsWidget(
            #     attrs={
            #         'class': '',
            #         'style': 'width: 100%',
            #     }
            # ),
        }
