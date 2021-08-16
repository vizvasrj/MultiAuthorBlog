from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import (
    get_object_or_404, render, redirect
)
from django.db.models import Count
from django.core.paginator import (
    Page,
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.contrib.auth.decorators import login_required


# local
from .models import Post, Category, Comment
from .forms import (
    PostForm, CommentForm
)
# 3rd party
from taggit.models import Tag


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = cd['tags']
            new_item = form.save(commit=False)
            new_item.author_id = request.user.id
            new_item.save()
            form.save_m2m()
            return redirect(new_item.get_absolute_url())
    else:
        form = PostForm(request.POST, request.FILES)
    
    return render(
        request,
        'blog/post_form.html',{
            'form': form,
        }
    )



def post_list(request, tag_slug=None, category_slug=None):
    posts = Post.published.all()
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag, slug=tag_slug
        )
        object_list = object_list.filter(
            tags__in=[tag]
        )
    paginator = Paginator(object_list, 10)
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
            'blog/post/list_ajax_main.html',{
                'posts': posts,
                'tag': tag
            }
        )
    return render(
        request,
        'blog/post/list.html',{
            'posts': posts,
            'tag': tag,

        }
    )


def post_detail(request, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
    )
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.commentor_id = request.user.id
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list(
        'id', flat=True
    )
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'blog/post/detail.html',{
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts
        }
    )
