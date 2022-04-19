from django import forms
# from django.db.models import fields
# from django.forms import widgets

from .models import Comment
from mptt.forms import TreeNodeChoiceField


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
        print(args, kwargs)

    class Meta:
        model = Comment
        fields = ('parent', 'body')
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'bg-dark',
                }
            ),
        }