from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.fields import CharField
from django.contrib.auth.forms import (
    PasswordResetForm, PasswordChangeForm

)
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


from .models import Profile



class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Username'),
        'type': 'text',
        'name': 'username'
    }))

    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Password'),
        'type': 'password',
        'name': 'password'
    }))


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Password ...'),
        'type': 'password',
        'name': 'password'
    }))
    password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Repeat Password ...'),
        'type': 'password',
        'name': 'password'
    }))
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Username ...'),
        'type': 'text',
        'name': 'username'
    }))

    email = forms.CharField(label=_('Email'), widget=forms.EmailInput(attrs={
        'class': 'myfieldclass ',
        'placeholder': _('Email ...'),
        'type': 'email',
        'name': 'email'
    }))



    class Meta:
        model = User
        fields = ('username', 'email')
        
        help_texts = {
            'username': '',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                _("Passwords doesn't Matched."))
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

        widgets = {
            'email': forms.TextInput(
                attrs={'rows': '4', 'cols': '50',
                        'class': 'myfieldclass'}
            ),
        }




class ProfileEditForm(forms.ModelForm):
    # photo = forms.ImageField(widget=forms.FileInput,)
    LANGUAGES = (
        ('en', 'English'),
        ('ar', 'عربي'),
        ('zh_hans', '简体中文'),
        ('tl', 'Filipino'),
        ('fr', 'français'),
        ('de', 'Deutsch'),
        ('hi', 'हिंदी'),
        ('id', 'bahasa Indonesia'),
        ('it', 'Italiana'),
        ('ja', '日本'),
        ('ko', '한국인'),
        ('nn', 'Norsk'),
        ('pt', 'Português'),
        ('ru', 'русский'),
        ('es', 'Española'),
        ('vi', 'Tiếng Việt'),
        ('bn', 'বাংলা'),
    )
    lang = forms.ChoiceField(label='Language', choices=LANGUAGES)
    class Meta:
        model = Profile
        fields = ('about', 'full_name', 'photo', 'lang')

        widgets = {
            'about': forms.Textarea(
                attrs={'rows': '3', 'cols': 'auto',
                        'class': 'myfieldclass'}
            ),
            'full_name': forms.TextInput(
                attrs={'rows': '3', 'cols': '50',
                        'class': 'myfieldclass'}
            ),
            'photo': forms.FileInput(
                attrs={'class': 'invisible'}
            ),
            'lang': forms.Select(
                attrs={
                    'class': 'lang'
                }
            )

        }


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label=_('Enter email address'), widget=forms.EmailInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Email ...'),
        'type': 'email',
        'name': 'email'
        }))


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    old_password = forms.CharField(label=_('Old password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Old password ...'),
        'type': 'password',
        'name': 'old_password'
    }))
    new_password1 = forms.CharField(label=_('New password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('New password ...'),
        'type': 'password',
        'name': 'new_password1'
    }))
    new_password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput(attrs={
        'class': 'myfieldclass',
        'placeholder': _('Repeat password ...'),
        'type': 'password',
        'name': 'new_password2'
    }))
    
    

class UserDeleteForm(forms.Form):
    password = forms.CharField(
        label=_('Enter Your password to delete your account'),
        widget=forms.PasswordInput(attrs={
            'class': 'delete_password',
            'placeholder': _('Enter your password to delete your account'),
            'type': 'password',
            'name': 'password'
        })
    )


class LanguageEditForm(forms.ModelForm):
    # photo = forms.ImageField(widget=forms.FileInput,)
    LANGUAGES = (
        ('en', 'English'),
        ('ar', 'عربي'),
        ('zh_hans', '简体中文'),
        ('tl', 'Filipino'),
        ('fr', 'français'),
        ('de', 'Deutsch'),
        ('hi', 'हिंदी'),
        ('id', 'bahasa Indonesia'),
        ('it', 'Italiana'),
        ('ja', '日本'),
        ('ko', '한국인'),
        ('nn', 'Norsk'),
        ('pt', 'Português'),
        ('ru', 'русский'),
        ('es', 'Española'),
        ('vi', 'Tiếng Việt'),
        ('bn', 'বাংলা'),

    )
    lang = forms.ChoiceField(label='Language', choices=LANGUAGES)
    class Meta:
        model = Profile
        fields = ('lang',)
        widgets = {
            'lang': forms.Select(
                attrs={
                    'class': 'lang'
                }
            )
        }



class LanguageSelect(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('lang',)
