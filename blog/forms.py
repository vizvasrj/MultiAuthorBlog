# core
from django import forms
from django.db.models import query
from django.forms import widgets

# local
from .models import Post, Comment

# 3rd party
from taggit.forms import TagWidget
from taggit_autosuggest.widgets import TagAutoSuggest
from mptt.forms import TreeNodeChoiceField
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2Widget
from django.utils import timezone, dateformat
from django.utils.timezone import localtime

from django.contrib.auth.models import User


from .models import Publication

lt = localtime(timezone.now())


# this will be usedn in publish value 
fomated_time = dateformat.format(lt, 'Y-m-d H:i')



# Select2

class CoAuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["username__istartswith", "email__icontains"]


class PostForm(forms.ModelForm):
    # publish = forms.DateField(
    #     widget=DatePickerInput(format='%m/%d/%Y')
    # )
    # publish = forms.DateTimeField(
    #     widget = DateTimePicker(
    #         options={
    #             'useCurrent': True,
    #             'collapse': False,
    #             # 'minDate': '2021-08-28',
    #             # 'maxDate': '2021-11-20',            
    #         },
    #         attrs={
    #             'append': 'fa fa-calendar',
    #             'icon_toggle': True,
    #         }
    #     )
    # )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Publish'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'myfieldclass bg-red-lite'}))
    publication = forms.ModelChoiceField(
        queryset=None, empty_label=None, to_field_name="id"
    )
    # other_author = forms.ModelChoiceField(
    #     queryset=None,
    #     widget=CoAuthorsWidget(
    #         model=User,
    #     )
    # )
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['publication'].queryset = Publication.objects.all().filter(editor=user.id)
        # if user != None:
        #     self.fields['other_author'].queryset = User.objects.exclude(id=user.id)

    class Meta:
        model = Post
        fields = (
            'title', 'body', 'tags', 'cover', 'status', 'publish',
            'other_author', 'publication'
        )
        widgets = {
            'title': forms.Textarea(
                attrs={'class': 'myfieldclass padding-15 border-bottom', 'autocomplete': 'off',
                'rows': "2", 'placeholder': 'Title'}
            ),
            'body': forms.Textarea(
                # config={'minHeight': 100}
                attrs={
                'placeholder': 'Type containt here.',
                    # 'class': 'myfieldclass ',
                }
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': 'Tags',
                    'required': False,
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'myfieldclass',
                    'required': False
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'bg-red',
                }
            ),
            'publish': forms.TextInput(
                attrs={
                    'class': 'myfieldclass text-center',
                    'value': fomated_time
                }
            ),

            'other_author': CoAuthorsWidget(
                attrs={
                    'class': 'bg-olive-lite',
                    'style': 'width: 100%',
                }
            )
            
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
    query = forms.CharField(label='Search', widget=forms.TextInput(attrs={
        'class': 'myfieldclass-search',
        'placeholder': 'Text here',
        'type': 'text',
        'name': 'search',
        'autocomplete': 'off'
    }))