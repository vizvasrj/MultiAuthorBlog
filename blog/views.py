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
    PostForm
)
# 3rd party
from taggit.models import Tag


@login_required
def create_post(request):
    user = request.user.profiles.full_name
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
            'user': user
        }
    )



def post_list(request, tag_slug=None, category_slug=None):
    posts = Post.published.all()
    object_list = Post.published.all()
    categories = Category.objects.annotate(
        total_category=Count('post_category')
    )
    tag = None
    if category_slug:
        category = get_object_or_404(
            Category,
            slug=category_slug
        )
        object_list = object_list.filter(
            category__in=[category]
        )
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
            'categories': categories

        }
    )