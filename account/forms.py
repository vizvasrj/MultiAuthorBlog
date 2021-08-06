from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.fields import CharField

from .models import Profile



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        

        widgets = {
            'email': forms.TextInput(
                attrs={'value': '', 'class': 'form'}
            ),
            'username': forms.TextInput(
                attrs={'value': '', 'class': 'form'}
            )
        }
        help_texts = {
            'username': '',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                'Passwords dosent Matched.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about', 'full_name', 'photo', 'color')
