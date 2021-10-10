from django.shortcuts import render
from .models import Publication as Publication, PublicationContact
from django.shortcuts import (
    get_object_or_404, render, redirect
)
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http.response import(
    HttpResponse, HttpResponseRedirect, JsonResponse
)
from django.urls import reverse
from blog.models import Post
from .forms import PubForm, ManageForm
# Create your views here.



@login_required
def publication_create_view(request):
    if request.method == 'POST':
        form = PubForm(
            user=request.user,

            data=request.POST, files=request.FILES
        )
        if form.is_valid():
            cd = form.cleaned_data
            new_item = cd['tags']
            new_item = form.save(commit=False)
            new_item.publisher_id = request.user.id
            new_item.save()
            form.save_m2m()
            return redirect(new_item.get_absolute_url())
    else:
        form = PubForm(
            user=request.user,

            data=request.POST, files=request.FILES
        )
    return render(
        request,
        'publication/publication_create.html',
        {'form': form,}
    )


def publication_list_view(request):
    pub = Publication.objects.all()
    return render(
        request,
        'publication/publication_list.html',{
            'pub': pub,
        }
    )

def publication_detail_view(request, slug):
    pub = get_object_or_404(
        Publication,
        slug=slug,
    )
    ratio = pub.image.height/pub.image.width
    # This will help to make not view trashed posts
    posts = Post.aupm.all().filter(publication=pub)
    # posts = pub.posts.all()
    paginator = Paginator(posts, 2)
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
            'publication/pub_post_list_ajax.html',{
                'posts': posts
            }
        )
    
    return render(
        request,
        'publication/publication_detail.html',{
            'pub': pub,
            'ratio': ratio,
            'posts': posts
        }
    )


@ajax_required
@require_POST
@login_required
def publication_follow(request):
    pub_id = request.POST.get('id')
    action = request.POST.get('action')
    if pub_id and action:
        try:
            pub = Publication.objects.get(id=pub_id)
            if action == 'follow':
                PublicationContact.objects.get_or_create(
                    user_from=request.user,
                    to_publication=pub
                )
            else:
                PublicationContact.objects.filter(
                    user_from=request.user,
                    to_publication=pub
                ).delete()
            return JsonResponse({'status': 'ok'})
        except Publication.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def editor_as_my_publication(request):
    pub = Publication.objects.all().filter(
        writer=request.user.id
    ).exclude(publisher=request.user.id)
    return render(
        request,
        'publication/my_publication/editor_my_publication.html', {
            'pub': pub
        }
    )

@login_required
def admin_as_my_publication(request):
    pub = Publication.objects.all().filter(
        publisher=request.user.id
    )
    return render(
        request,
        'publication/my_publication/admin_my_publication.html',{
            'pub': pub
        }
    )


@login_required
def my_publication_list(request):
    p_owner = Publication.objects.all().filter(
        publisher=request.user.id
    )
    p_writer = Publication.objects.all().filter(
        writer=request.user.id
    ).exclude(publisher=request.user.id)
    p_following = Publication.objects.all().filter(
        followers=request.user.id
    )

    paginator = Paginator(p_following, 10)
    page = request.GET.get('page')
    try:
        p_following = paginator.page(page)
    except PageNotAnInteger:
        p_following = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        p_following = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(
            request,
            'publication/me/publication_follow_list_ajax.html',{
                'p_following': p_following
            }
        )

    return render(
        request,
        'publication/me/publications.html', {
            'p_following': p_following,
            'p_owner': p_owner,
            'p_writer': p_writer
        }
    )


@ajax_required
@require_POST
@login_required
def publication_leave(request):
    pub_id = request.POST.get('id')
    if pub_id:
        try:
            pub = Publication.objects.get(id=pub_id)
            pub.writer.remove(request.user.id)
            return JsonResponse({'status': 'ok'})
        except Publication.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def manage_publication(request, pk):
    pub = get_object_or_404(
        Publication,
        # slug=slug
        pk = pk
    )
    form = ManageForm(
        user=request.user,
        data=request.POST,
        files=request.FILES,
        instance=pub
    )
    if request.user.id == pub.publisher_id:
        if request.method == 'POST':
            if form.is_valid():
                pub = form.save(commit=False)
                pub.publisher_id = request.user.id
                pub.save()
                form.save_m2m()
                return redirect(pub.get_absolute_url())
        else:
            form = ManageForm(
                user=request.user,
                instance=pub
            )
        return render(
            request,
            'publication/manage.html', {
                'form': form,
                'pub': pub
            }
        )
    else:
        return HttpResponseRedirect(reverse('publication_list'))
    

@login_required
def me_writer(request):
    pub = Publication.objects.all().filter(
        writer=request.user.id
    )
    return render(
        request,
        'publication/me/writer/writer.html',{
            'pub': pub
        }
    )


@login_required
def me_publisher(request):
    pub = Publication.objects.all().filter(
        publisher=request.user.id
    )
    return render(
        request,
        'publication/me/writer/writer.html',{
            'pub': pub
        }
    )


