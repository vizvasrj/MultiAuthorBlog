# core
from django import forms


# local
from .models import Post, Comment

# 3rd party
from taggit_autosuggest.widgets import TagAutoSuggest
from mptt.forms import TreeNodeChoiceField
# from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django_select2 import forms as s2forms
from django.utils import timezone, dateformat
from django.utils.timezone import localtime

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from publication.models import Publication as Pub
from blog.models import SharedOrOtherEdit

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
        queryset=None, 
        required=False,
        to_field_name="id", 
        empty_label=_("No Publication"),
        widget=forms.Select(
                attrs={
                    'class': 'myfieldclass bg-red-lite',
                }
            ),
    )
    # other_author = forms.ModelChoiceField(
    #     queryset=None,
    #     widget=CoAuthorsWidget(
    #         model=User,
    #     )
    # )
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['publication'].queryset = Pub.objects.all().filter( Q(writer=user.id) | Q(publisher=user.id))
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
                'rows': "2", 'placeholder': _('Title')}
            ),
            'body': forms.Textarea(
                # config={'minHeight': 100}
                attrs={
                'placeholder': _('Type content here.'),
                    'class': 'myfieldclass ',
                }
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': _('Tags'),
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
            ),
            'publication': forms.Select(
                attrs={
                    'class': 'myfieldclass bg-red-lite',
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
    query = forms.CharField(label='Search', widget=forms.TextInput(attrs={
        'class': 'myfieldclass-search',
        'placeholder': _('Text here'),
        'type': 'text',
        'name': 'search',
        'autocomplete': 'off'
    }))


class PubForm(forms.ModelForm):
    
    class Meta:
        model = Pub
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
            'editor': CoAuthorsWidget(
                attrs={
                    'class': '',
                    'style': 'width: 100%',
                }
            ),
        }

class OtherEditForm(forms.ModelForm):

    class Meta:
        model = SharedOrOtherEdit
        fields = ('title', 'body', 'edit_summary', 'tags')
        

class TranslatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title', 'body', 'tags', 'cover',
        )
        widgets = {
            'title': forms.Textarea(
                attrs={'class': 'myfieldclass padding-15 border-bottom', 'autocomplete': 'off',
                'rows': "2", 'placeholder': _('Title')}
            ),
            'body': forms.Textarea(
                # config={'minHeight': 100}
                attrs={
                'placeholder': _('Type content here.'),
                    'class': 'myfieldclass ',
                }
            ),
            'tags': TagAutoSuggest('tagmodel',
                attrs={
                    'class': 'myfieldclass border-bottom p-2 tag_label inputTag',
                    'autocomplete': 'off',
                    'placeholder': _('Tags'),
                    'required': False,
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'myfieldclass',
                    'required': False
                }
            ),
            # 'status': forms.Select(
            #     attrs={
            #         'class': 'bg-red',
            #     }
            # ),
            # 'publish': forms.TextInput(
            #     attrs={
            #         'class': 'myfieldclass text-center',
            #         'value': fomated_time
            #     }
            # ),

            # 'other_author': CoAuthorsWidget(
            #     attrs={
            #         'class': 'bg-olive-lite',
            #         'style': 'width: 100%',
            #     }
            # ),
            # 'publication': forms.Select(
            #     attrs={
            #         'class': 'myfieldclass bg-red-lite',
            #     }
            # ),
            
        }


