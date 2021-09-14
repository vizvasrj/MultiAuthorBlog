import re
from django.http.response import(
    HttpResponse, HttpResponseRedirect, JsonResponse
)
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
from django.urls import reverse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.contrib.postgres.search import(
    SearchQuery, SearchVector, SearchRank
)
from django.utils import timezone

# local
from .models import Post, Category, Comment
from .forms import (
    PostForm, CommentForm, SearchForm
)
# 3rd party
from taggit.models import Tag
import redis
from django.conf import settings
# Connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)



@login_required
def create_post(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = cd['tags']
            new_item = form.save(commit=False)
            new_item.author_id = request.user.id
            # eltetime ok iwill set now
            deltatime = new_item.publish + timezone.timedelta(minutes=1)
            if deltatime >= timezone.localtime(timezone.now()):
                new_item.save()
                form.save_m2m()
                return redirect(new_item.get_absolute_url())
            else:
                new_item.publish = timezone.localtime(timezone.now())
                new_item.save()
                form.save_m2m()
                return redirect(new_item.get_absolute_url())
    else:
        form = PostForm(request.POST, request.FILES)

    return render(
        request,
        'blog/post_form.html', {
            'form': form,
            'user': user,
        }
    )


def post_list(request, tag_slug=None):
    # posts = Post.published.all()
    object_list = Post.aupm.all()
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
            'blog/post/list_ajax.html', {
                'posts': posts,
                'tag': tag
            }
        )
    return render(
        request,
        'blog/post/list.html', {
            'posts': posts,
            'tag': tag,

        }
    )


def post_detail(request, post):
    post = get_object_or_404(
        Post,
        slug=post,
    )
    total_views = r.incr(f'post:{post.id}:views')
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.commentor_id = request.user.id
            new_comment.save()
            return HttpResponseRedirect('')
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
        'blog/post/detail.html', {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
            'total_views': total_views,
        }
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', 'body'
            )
            search_query = SearchQuery(query)
            results = Post.published.filter(
                status="published"
            ).filter(
                publish__lte=timezone.now()
            ).annotate(
                search=search_vector,
                rank=SearchRank(
                    search_vector, search_query
                )
            ).filter(search=search_query).order_by('-rank')
    paginator = Paginator(results, 2)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        results = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'blog/search/list_ajax.html', {
                'results': results,
            }
        )
    return render(
        request,
        'blog/search/search.html', {
            'form': form,
            'query': query,
            'results': results
        }
    )


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(
        Post,
        id=comment.post.id
    )
    form = CommentForm(
        request.POST or None,
        instance=comment
    )
    if request.user.id == comment.commentor_id:
        if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post_id = post.id
                comment.commentor_id = request.user.id
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            form = CommentForm(instance=comment)
        return render(
            request,
            'blog/comment/update.html', {
                'form': form,
                'post': post
            }
        )
    else:
        return HttpResponseRedirect(reverse('404'))


@ajax_required
@login_required
@require_POST
def comment_like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            if action == 'like':
                comment.users_like.add(request.user)
            else:
                comment.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@ajax_required
@login_required
@require_POST
def bookmark(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            post.title
            if action == 'bookmark':
                post.bookmark_list.add(request.user)
            else:
                post.bookmark_list.remove(request.user)
            return JsonResponse({
                'title': post.title,
                'status': 'ok'
            })
        except:
            pass
    return JsonResponse({'status': 'ok'})

from django.utils.timezone import localtime
from django.utils import timezone, dateformat


lt = localtime(timezone.now())


# this will be usedn in publish value 
fomated_time = dateformat.format(lt, 'Y-m-d H:i')



@login_required
def update_data(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.publish = fomated_time
    # post.save()
    # loading cover image to edit post page
    if post.cover:
        cover_image = post.cover.url
    else:
        cover_image = 'No image'
    # main author is the one who created the post
    # in this i am checking that auther is present in shared post
    # if user is present then give the permission to edit it.
    main_author_id = post.author.id
    shared_user = []
    for s_user in Post.objects.get(id=pk).other_author.all():
        shared_user.append(s_user.id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post
    )
    if request.user.id == post.author_id:
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.author_id = request.user.id
                post.last_editeduser_id = request.user.id
                post.save()
                form.save_m2m()
                for x in post.other_author.all():
                    print(x)
                return redirect(post.get_absolute_url())
        else:
            form = PostForm(instance=post)
        return render(
            request,
            'blog/post_update.html',
            {'form': form, 'cover_image': cover_image, 'status': 'Publish'}
        )
    elif request.user.id in shared_user:
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.author_id = main_author_id
                post.last_editeduser_id = request.user.id
                post.status = 'draft'
                post.save()
                form.save_m2m()
                return redirect(post.get_absolute_url())
        else:
            form = PostForm(instance=post)
        return render(
            request,
            'blog/post_update.html',
            {'form': form, 'cover_image': cover_image, 'status': 'Save'}
        )
    else:
        return HttpResponseRedirect(reverse('404'))


@login_required
def delete_post(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    if request.user.id == instance.author_id:
        instance.delete()
        return HttpResponseRedirect(
            reverse('user_detail', args=[
                request.user.username
            ])
        )
    else:
        return HttpResponseRedirect(
            reverse('404')
        )


def tag_list(request, post_id=None):
    tags = Tag.objects.all()
    object_list = Tag.objects.all()
    post = None
    if post_id:
        post = get_object_or_404(
            Post,
            id=post_id
        )
        object_list = object_list.filter(
            post__in=[post]
        )

    paginator = Paginator(tags, 10)
    page = request.GET.get('page')
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        tags = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'blog/tag/list_ajax.html', {
                'tags': tags,
                'post': post,
            }
        )
    return render(
        request,
        'blog/tag/list.html', {
            'tags': tags,
            'post': post
        }
    )


def tag_detail(request, tag):
    tag = get_object_or_404(
        Tag,
        slug=tag,
    )

from easy_thumbnails.files import get_thumbnailer

@ajax_required
@require_POST
def post_ajax_search(request):
    if request.is_ajax():
        res = None
        post = request.POST.get('post')
        print(post)
        query = post
        search_vector = SearchVector(
            'title', 'body', 'author'
        )
        search_query = SearchQuery(query)
        results = Post.published.annotate(
            search=search_vector,
            rank=SearchRank(
                search_vector, search_query
            )
        ).filter(search=search_query).filter(
            publish__lte=timezone.now()    
        ).order_by('-rank')
        qs = results
        print(qs)
        if len(qs) > 0 and len(post) > 0:
            data = []
            for pos in qs:
                item = {
                    'slug': pos.slug,
                    'title': pos.title,
                    'cover': get_thumbnailer(pos.cover).get_thumbnail({
                        'size': (50, 50),
                        'crop': True,
                    }).url
                    # 'author': pos.author.user,
                }
                data.append(item)
            res = data[:10]
        else:
            res = "No posts found ..."
        return JsonResponse({'data': res})
    return JsonResponse({})
