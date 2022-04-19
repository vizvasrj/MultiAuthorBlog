from blog.models import Comment
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import AboutPost
from django.core.paginator import (
    Page, PageNotAnInteger, EmptyPage, Paginator
)

from comment.forms import CommentForm
from comment.models import Comment

import redis
from django.conf import settings
from common.utils import is_ajax

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
        if is_ajax(request=request):
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if is_ajax(request=request):
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
    if about_post.comment_active is True:
        comments = about_post.comments.filter(active=True)
        # Paginator starts [commnets]
        # comments = comments.get_descendants(include_self=True)
        # paginator = Paginator(comments, 6)
        # page = request.GET.get('page')
        # try:
        #     comments = paginator.page(page)
        # except PageNotAnInteger:
        #     comments = paginator.page(1)
        # except EmptyPage:
        #     if is_ajax(request=request):
        #         return HttpResponse('')
        #     comments = paginator.page(paginator.num_pages)
        # if is_ajax(request=request):
        #     return render(
        #         request,
        #         'about/comment/list_ajax.html', {
        #             'comments': comments,
        #             'about_post': about_post,
        #         }
        #     )
    # paginator Ends
        # print(colored(comments, 'red'))
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
                # print(colored(new_comment.parent, 'red'))
                try:
                    # print(colored(new_comment.parent.get_ancestors().count(), 'blue'))
                    if new_comment.parent.get_ancestors().count() >= settings.MAX_COMMENT_TREE:
                        pass
                    else:
                        new_comment.save()
                except AttributeError:
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
    else:
        return render(
            request,
            'about/post/detail.html', {
                'about_post': about_post,
                'total_views': total_views,
            }
        )


def contact_us(request):
    contact_us = AboutPost.objects.filter(category='c').order_by('-created')[0]

    return render(
        request,
        'about/post/detail.html',{
            'about_post': contact_us
        }
    )

