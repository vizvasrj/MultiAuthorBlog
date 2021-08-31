# django
from datetime import date
from django.contrib import auth
from django.core import paginator
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import (
    EmptyPage,
    Page,
    PageNotAnInteger,
    Paginator)
from django.shortcuts import get_object_or_404
from django.urls import reverse

# 3rd party


# local
from .models import Profile, Contact
from .forms import (
    LoginForm, UserRegistrationForm,
    UserEditForm, ProfileEditForm
)
from django.views.decorators.http import require_POST
from common.decorators import ajax_required

from blog.models import Post

def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('post_list'))
    else:
        next = ""
        if request.GET:
            next = request.GET['next']
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user_k = cd['username']
                user = authenticate(
                    request,
                    username=cd['username'],
                    password=cd['password']
                )
                if user is not None:
                    if user.is_active:
                        last_user_login = User.objects.get(
                            username=user_k
                        ).last_login
                        if last_user_login:
                            if next != "":
                                login(request, user)
                                return HttpResponseRedirect(request.GET['next'])
                            else:
                                login(request, user)
                                return redirect(reverse('post_list'))
                        else:
                            login(request, user)
                            return redirect(reverse('edit'))

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


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('post_list'))
    else:
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(
                    user_form.cleaned_data['password1']
                )
                new_user.save()
                Profile.objects.create(user=new_user)
                return render(
                    request,
                    'account/register_done.html',
                    {'new_user': new_user}
                )
        else:
            user_form = UserRegistrationForm()
        return render(
            request,
            'account/register.html',
            {'user_form': user_form}
        )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profiles,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and \
                profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Profile updated successfully'
            )
        else:
            messages.error(
                request,
                'Error updating your profile'
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profiles
        )
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


def user_list(request):
    object_list = User.objects.filter(is_active=True)
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        users = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/user/user_list.html',
            {'users': users}
        )

    return render(
        request,
        'account/user/list.html',
        {'users': users}
    )

def user_detail(request, username):
    user = get_object_or_404(
        User,
        username=username,
        is_active=True
    )
    object_list = user.profiles.blog_posts.filter(
        status="published").filter(
            publish__lte=timezone.now()).all()
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/user/user_post_list_ajax.html', {
                'posts': posts,
                'user': user
            }
        )
    return render(
        request,
        'account/user/detail.html',
        {'user': user, 'posts': posts}
    )


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def me_page(request):
    # me = User.objects.get(username=request.user.username)
    return redirect(reverse('user_detail', args=[request.user]))


# @login_required
# def me(request):
#     user = get_object_or_404(
#         User,
#         username=request.user.username,
#         is_active=True
#     )
#     return render(
#         request,
#         'account/user/detail.html',
#         {'user': user}
#     )
def me(request):
    user = get_object_or_404(
        User,
        username=request.user.username,
        is_active=True
    )
    object_list = user.profiles.blog_posts.filter(
        status="published").filter(
            publish__lte=timezone.now()).all()
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/user/user_post_list_ajax.html', {
                'posts': posts,
                'user': user
            }
        )
    return render(
        request,
        'account/user/detail.html',
        {'user': user, 'posts': posts}
    )



def user_following(request, username):
    user = get_object_or_404(
        User,
        username=username,
        is_active=True
    )
    object_list = user.rel_from_set.all()
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        following = paginator.page(page)
    except PageNotAnInteger:
        following = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        following = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/user/following_list.html',
            {'following': following}
        )
    return render(
        request,
        'account/user/following.html',
        {'following': following, 'user': user}
    )


def user_follower(request, username):
    user = get_object_or_404(
        User,
        username=username,
        is_active=True
    )
    object_list = user.rel_to_set.all()
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        follower = paginator.page(page)
    except PageNotAnInteger:
        follower = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        follower = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/user/follower_list.html',
            {'follower': follower}
        )
    return render(
        request,
        'account/user/follower.html',
        {'follower': follower, 'user': user}
    )


@login_required
def my_published_stories(request):
    me = Profile.objects.get(user_id=request.user.id)
    # me_posts = me.objects.all()
    object_list = me.blog_posts.filter(status="published").all()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/me/my_post_list_ajax.html', {
                'posts': posts
            }
        )
    return render(
        request,
        'account/me/my_posts.html', {
            'posts': posts,
            'status' : 'published'
        }
    )

@login_required
def my_drafted_stories(request):
    me = Profile.objects.get(user_id=request.user.id)
    # me_posts = me.objects.all()
    object_list = me.blog_posts.filter(status="draft").all()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/me/my_post_list_ajax.html', {
                'posts': posts,
            }
        )
    return render(
        request,
        'account/me/my_posts.html', {
            'posts': posts,
            'status': 'drafted'
        }
    )

@login_required
def my_trashed_stories(request):
    me = Profile.objects.get(user_id=request.user.id)
    # me_posts = me.objects.all()
    object_list = me.blog_posts.filter(status="trashed").all()
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'account/me/my_post_list_ajax.html', {
                'posts': posts
            }
        )
    return render(
        request,
        'account/me/my_posts.html', {
            'posts': posts,
            'status': 'trashed'
        }
    )


@ajax_required
@require_POST
@login_required
def trash_post(request):
    post_id = request.POST.get('id')
    instance = get_object_or_404(Post, id=post_id)
    if post_id:
        try:
            if request.user.id == instance.author_id:
                instance.status = 'trashed'
                instance.save()
                return JsonResponse({'status': 'ok'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=404)


@ajax_required
@require_POST
@login_required
def delete_post(request):
    post_id = request.POST.get('id')
    instance = get_object_or_404(Post, id=post_id)
    if post_id:
        try:
            if request.user.id == instance.author_id:
                instance.delete()
                return JsonResponse({'status': 'ok'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=404)

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.utils import timezone

@ajax_required
@require_POST
@login_required
def publish_post(request):
    post_id = request.POST.get('id')
    date_input = request.POST.get('datetime')
    parsed_date = parse_datetime(date_input)
    # Checking date for 4 minute before
    aware_date = make_aware(parsed_date)
    deltatime = aware_date + timezone.timedelta(minutes=4)
    instance = get_object_or_404(Post, id=post_id)
    if post_id:
        try:
            if request.user.id == instance.author_id:
                instance.status = 'published'
                if deltatime >= timezone.localtime(timezone.now()):
                    instance.publish = aware_date
                    instance.save()
                    return JsonResponse({'status': 'ok'}, status=200)
                else:
                    instance.publish = timezone.localtime(timezone.now())
                    instance.save()
                    return JsonResponse({'status': 'ok'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=404)


@ajax_required
@require_POST
@login_required
def untrash_post(request):
    post_id = request.POST.get('id')
    instance = get_object_or_404(Post, id=post_id)
    if post_id:
        try:
            if request.user.id == instance.author_id:
                instance.status = 'draft'
                instance.save()
                return JsonResponse({'status': 'ok'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'status': 'not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=404)
