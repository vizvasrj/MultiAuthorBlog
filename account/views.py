# django
from django.contrib import auth
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

# 3rd party


# local
from .models import Profile, Contact
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(
                        'Authentication Successfull'
                    )
                else:
                    return HttpResponse(
                        'Disabled Account'
                    )
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(
        request,
        'account/login.html',
        {'form': form}
    )