from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class UserRegistrationForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    repeat_password = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_reset_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['reset_password']:
            raise forms.ValidationError(
                'Passwords dosent Matched.')
        return cd['reset_password']

