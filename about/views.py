from blog.models import Comment
from django.core import paginator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import AboutPost
from django.core.paginator import (
    Page, PageNotAnInteger, EmptyPage, Paginator
)

from comment.forms import CommentForm
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType

import redis
from django.conf import settings
from termcolor import colored

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

# Create your views here.


def about_post_list_view(request):
    posts = AboutPost.objects.all()
    paginator = Paginator(posts, 10)
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
            'about/post/list_ajax.html', {
                'posts': posts,
            }
        )
    return render(
        request,
        'about/post/list.html', {
            'posts': posts
        }
    )


def about_post_detail(request, slug):
    about_post = get_object_or_404(
        AboutPost,
        slug=slug
    )
    total_views = r.incr(f'about_post:{about_post.id}:views')
    # content_type = ContentType.objects.get(app_label='about', model='AboutPost')
    comments = about_post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(
            request.POST, request.FILES
        )
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment = Comment(
                body=new_comment.body,
                content_object=about_post,
                parent=new_comment.parent
            )
            # new_comment.about_post = about_post
            new_comment.commentor_id = request.user.id
            print(colored(new_comment.parent, 'red'))
            print(colored(new_comment.parent.get_ancestors().count(), 'blue'))
            if new_comment.parent.get_ancestors().count() >= settings.MAX_COMMENT_TREE:
                pass
            else:
                new_comment.save()

            return HttpResponseRedirect('')
    else:
        comment_form = CommentForm()

    return render(
        request,
        'about/post/detail.html', {
            'about_post': about_post,
            'comments': comments,
            'new_comment': new_comment,
            'total_views': total_views,
        }
    )