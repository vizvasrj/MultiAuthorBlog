from datetime import timedelta
from django.contrib import auth
from django.db.models.query import InstanceCheckMeta
from easy_thumbnails.files import get_thumbnailer
from django.utils.timezone import localtime
from django.utils import timezone, dateformat
import re
from django.http.response import(
    HttpResponse, HttpResponseRedirect, JsonResponse
)
from django.shortcuts import render
from django.shortcuts import (
    get_object_or_404, render, redirect
)
from django.db.models import Count, F
from django.core.paginator import (
    Page,
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
import requests
from common.decorators import ajax_required
from django.contrib.postgres.search import(
    SearchQuery, SearchVector, SearchRank
)
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from .models import MyCustomTag, Post, Comment, TagContact
from .forms import (
    PostForm, CommentForm, SearchForm,
    )
# 3rd party
from taggit.models import Tag
import redis
from nltk.corpus import wordnet


from django.core.cache import cache
a_timedelta = timedelta(minutes=1)

on_day_in_seconds = a_timedelta.total_seconds()

from .tasks import tag_main

# Connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

# delta time check on time given by user
def delta_time(time):
    delta = time + timezone.timedelta(minutes=1)
    if delta >= timezone.localtime(timezone.now()):
        return time
    else:
        return timezone.localtime(timezone.now())

@login_required
def create_post(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(user=request.user, data=request.POST,
                        files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = cd['tags']
            new_item = form.save(commit=False)
            new_item.author_id = request.user.id
            new_item.publish = delta_time(time=new_item.publish)
            new_item.save()
            form.save_m2m()
            return redirect(new_item.get_absolute_url())
    else:
        form = PostForm(user=request.user, data=request.POST,
                        files=request.FILES)
    return render(
        request,
        'blog/post_form.html', {
            'form': form,
            'user': user,
        }
    )


def post_list(request, tag_slug=None):
    # posts = Post.published.all()
    posts = Post.aupm.all()
    print(translation.get_language_from_request(request))
    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag, slug=tag_slug
        )
        posts = posts.filter(
            tags__slug__in=[tag]
        )
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

# This is used to increase tag value
# def tag_val_inc(request, slug):
#     user = User.objects.get(id=request.user.id)
#     print(slug, "slug")
#     tag = MyCustomTag.objects.get(slug=slug)
#     tag_name = TagNameValue.objects.filter(tag__slug=slug, user=user)
#     if tag_name.exists():
#         tag_name.update(value=F('value')+1)
#     else:
#         tag_name = TagNameValue.objects.get_or_create(
#             tag=tag,
#             user=user,
#             value=1
#         )

from django.utils import translation
import requests
import datetime

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60    # one year
    else:
        max_age = days_expire * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )


def active_translate(value):
    if value in {'IN', 'NP'}:
        translation.activate('hi')
    elif value in {'US', 'UK', 'AG', 'AU',
                    'BS', 'BB', 'BZ', 'BW',
                    'CA', 'DM', 'FJ', 'GM',
                    'GH', 'GD', 'GY', 'IE',
                    'JM', 'KE', 'KI', 'LS',
                    'LR', 'MW', 'MT', 'MH',
                    'MU', 'FM', 'NA', 'NR',
                    'NZ', 'NG', 'PW', 'PG',
                    'RW', 'KN', 'LC', 'VC',
                    'WS', 'SL', 'SG', 'SB',
                    'ZA', 'SS', 'SD', 'SZ',
                    'TZ', 'TO', 'TT', 'TV',
                    'UG', 'VU', 'ZM', 'ZW'}:
        translation.activate('en')
    elif value in {'FR', 'BE', 'BJ', 'BF',
                    'BI', 'CF', 'TD', 'KM', 
                    'CD', 'CG', 'CI', 'DJ',
                    'GA', 'GN', 'LU', 'MG',
                    'ML', 'MC', 'NE', 'SN',
                    'SC', 'TG'}:
        translation.activate('fr')
    elif value in {'DZ', 'EG', 'IQ', 'IL',
                    'JO', 'KW', 'LB', 'LY',
                    'MR', 'MA', 'OM', 'QA',
                    'SA', 'SO', 'SY', 'TN',
                    'AE', 'YE'}:
        translation.activate('ar')
    elif value in {'AO', 'BR', 'CV', 'TL', 
                    'GW', 'MZ', 'PT', 'ST'}:
        translation.activate('pt')
    elif value in {'BY', 'RU', 'KZ', 'KG'}:
        translation.activate('ru')
    elif value in {'PH'}:
        translation.activate('ta')
    elif value in {'DE', 'AT', 'LI', 'CH'}:
        translation.activate('de')
    elif value in {'ID'}:
        translation.activate('id')
    elif value in {'IT', 'SM', 'VA'}:
        translation.activate('it')
    elif value in {'JP'}:
        translation.activate('ja')
    elif value in {'VN'}:
        translation.activate('vi')
    elif value in {'AD', 'AR', 'BO', 'CL',
                    'CO', 'CR', 'CU', 'DO',
                    'EC', 'SV', 'GQ', 'GT',
                    'HN', 'MX', 'NI', 'PA',
                    'PY', 'PE', 'ES', 'UY',
                    'VE'}:
        translation.activate('es')
    elif value in {'CN'}:
        translation.activate('zh-hans')
    elif value in {'KR', 'KP'}:
        translation.activate('ko')
    elif value in {'NO'}:
        translation.activate('nn')
    else:
        translation.activate('en')



def post_detail(request, slug, author):
    # FOr IP
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    
    # curl = requests.get(f'http://ip-api.com/csv/{ip}?fields=countryCode')
    # text = curl.text
    # country_code = text.split('\n')[0]
    # ip = country_code
    # if ip == 'IN':
    #     ip = 'hi'
    
    value = request.COOKIES.get('cookie_name_user')
    if value is None:
        # Cookie is not set
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        curl = requests.get(f'http://ip-api.com/csv/{ip}?fields=countryCode')
        text = curl.text
        country_code = text.split('\n')[0]

        # response.set_cookie('cookie_name', country_code)
        # this function will be used to make cookie
        response = HttpResponse("hello")

        set_cookie(response, 'cookie_name_user', country_code, 1)
        value = country_code
            
    active_translate(value)
    print(value, "VAUE after SET COKKIE")

    user = request.user
    language = request.LANGUAGE_CODE
    cache.delete(f'post-{slug}')
    post = cache.get(f'post-{slug}')        
    if not post:
        post = get_object_or_404(
            Post,
            slug=slug,
        )
        # print(f'{slug} not in cache')
        cache.set(f'post-{slug}', post, on_day_in_seconds) 
    else:
        # print(f'{slug} get from cache')
        pass
    # r.set(f"idid_post", bytes(post))
    if language == 'en':
        if post.english_translated_post.last():
            t_post = post.english_translated_post.last()
        else:
            t_post = post

    elif language == 'zh-hans':
        if post.chinese_translated_post.last():
            t_post = post.chinese_translated_post.last()
        else:
            t_post = post

    elif language == 'hi':
        if post.hindi_translated_post.last():
            t_post = post.hindi_translated_post.last()
        else:
            t_post = post
        
    elif language == 'ar':
        if post.arabic_translated_post.last():
            t_post = post.arabic_translated_post.last()
        else:
            t_post = post

    elif language == 'ta':
        if post.filipino_translated_post.last():
            t_post = post.filipino_translated_post.last()
        else:
            t_post = post

    elif language == 'fr':
        if post.french_translated_post.last():
            t_post = post.french_translated_post.last()
        else:
            t_post = post
    
    elif language == 'de':
        if post.german_translated_post.last():
            t_post = post.german_translated_post.last()
        else:
            t_post = post
    
    elif language == 'id':
        if post.indonesian_translated_post.last():
            t_post = post.indonesian_translated_post.last()
        else:
            t_post = post
    
    elif language == 'it':
        if post.italian_translated_post.last():
            t_post = post.italian_translated_post.last()
        else:
            t_post = post

    elif language == 'ja':
        if post.japanese_translated_post.last():
            t_post = post.japanese_translated_post.last()
        else:
            t_post = post
    
    elif language == 'ko':
        if post.korean_translated_post.last():
            t_post = post.korean_translated_post.last()
        else:
            t_post = post
    
    elif language == 'nn':
        if post.norwegian_translated_post.last():
            t_post = post.norwegian_translated_post.last()
        else:
            t_post = post

    elif language == 'pt':
        if post.portuguese_translated_post.last():
            t_post = post.portuguese_translated_post.last()
        else:
            t_post = post

    elif language == 'ru':
        if post.russian_translated_post.last():
            t_post = post.russian_translated_post.last()
        else:
            t_post = post
    
    elif language == 'es':
        if post.spanish_translated_post.last():
            t_post = post.spanish_translated_post.last()
        else:
            t_post = post
    
    elif language == 'vi':
        if post.vietnamese_translated_post.last():
            t_post = post.vietnamese_translated_post.last()
        else:
            t_post = post
    # I know it will never get inside this else statement
    else:
        # print('inside else')
        t_post = post

    # print(t_post.title)
    # print(t_post)
    # IP
    # ip = request.META.get("REMOTE_ADDR")

    if request.user.is_authenticated:
        user = request.user
        # i think this is better on celery
        # background task slow tasks
        tag_main.delay(user=user.id, post=post.id)

    else:
        pass
        
    # num_visits = request.session.get('num_visits', 0) + 1
    # request.session['num_visits'] = num_visits
    # print(str(num_visits))
    # print(request.COOKIES['sessionid'])


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
    similar_posts = Post.aupm.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    if similar_posts:
        pass
    else:
        similar_posts = Post.aupm.all().order_by('-created')
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
            't_post': t_post,
            'value': value
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


lt = localtime(timezone.now())
# this will be usedn in publish value
fomated_time = dateformat.format(lt, 'Y-m-d H:i')


@login_required
def update_data(request, pk):
    
    post = get_object_or_404(Post, pk=pk)
    cache.delete(f'post-{post.slug}')   

    # post.publish = fomated_time
    # post.save()
    # loading cover image to edit post page
    if post.cover:
        cover_image = post.cover.url
    else:
        cover_image = 'No image'
    tags = []
    for tag in post.tags.all():
        tags.append(tag.name)
    tags = ",".join(tags)
    # main author is the one who created the post
    # in this i am checking that auther is present in shared post
    # if user is present then give the permission to edit it.
    main_author_id = post.author.id
    shared_user = []
    for s_user in Post.objects.get(id=pk).other_author.all():
        shared_user.append(s_user.username)
    form = PostForm(user=request.user, data=request.POST,
                    files=request.FILES, instance=post)
    if (request.user.id == post.author_id or request.user.username in shared_user):
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                if request.user.id == post.author_id:
                    post.status = 'published'
                    post.author_id = main_author_id
                else:
                    post.author_id = main_author_id
                    post.status = 'draft'
                post.last_editeduser_id = request.user.id
                post.publish = delta_time(time=post.publish)
                post.save()
                form.save_m2m()
                return redirect(post.get_absolute_url())
        else:
            form = PostForm(user=request.user, instance=post)
        return render(
            request,
            'blog/post_update.html',
            {
                'form': form,
                'cover_image': cover_image,
                # 'status': 'Publish',
                'tags': tags,
                'fomated_time': fomated_time,
            }
        )
    else:
        return HttpResponse(_('Your are not authorized to edit :)'))


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


@ajax_required
@require_POST
def post_ajax_search(request):
    if request.is_ajax():
        res = None
        post = request.POST.get('post')
        # print(post)
        query = post
        search_vector = SearchVector(
            'title',
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
                try:
                    pos_cover = get_thumbnailer(pos.cover).get_thumbnail({
                        'size': (50, 50),
                        'crop': True,
                    }).url
                except:
                    pos_cover = None
                item = {
                    'slug': pos.slug,
                    'title': pos.title,
                    'cover': pos_cover,
                    # 'author': pos.author.user,
                }
                data.append(item)
            res = data[:10]
        else:
            res = _("No posts found ...")
        return JsonResponse({'data': res})
    return JsonResponse({})


# from translates.hindi_translate.models import HindiTranslatedPost as hi_p
# from translates.arabic_translate.models import ArabicTranslatedPost as ar_p
# from translates.chinese_translate.models import ChineseTranslatedPost as cn_p
# from translates.filipino_translate.models import FilipinoTranslatedPost as tl_p
# from translates.french_translate.models import FrenchTranslatedPost as fr_p
# from translates.german_translate.models import GermanTranslatedPost as de_p
# from translates.indonesian_translate.models import IndonesianTranslatedPost as id_p
# from translates.italian_translate.models import ItalianTranslatedPost as it_p
# from translates.japanese_translate.models import JapaneseTranslatedPost as jp_p
# from translates.korean_translate.models import KoreanTranslatedPost as ko_p
# from translates.norwegian_translate.models import NorwegianTranslatedPost as no_p
# from translates.portuguese_translate.models import PortugueseTranslatedPost as pt_p
# from translates.russian_translate.models import RussianTranslatedPost  as ru_p
# from translates.spanish_translate.models import SpanishTranslatedPost as es_p
# from translates.vietnamese_translate.models import VietnameseTranslatedPost as vi_p


def translate_listview(request, post):
    post = get_object_or_404(
        Post,
        slug=post,
    )
    cn_p = post.chinese_translated_post.last()
    hi_p = post.hindi_translated_post.last()
    ar_p = post.arabic_translated_post.last()
    tl_p = post.filipino_translated_post.last()
    fr_p = post.french_translated_post.last()
    de_p = post.german_translated_post.last()
    id_p = post.indonesian_translated_post.last()
    it_p = post.italian_translated_post.last()
    jp_p = post.japanese_translated_post.last()
    ko_p = post.korean_translated_post.last()
    no_p = post.norwegian_translated_post.last()
    pt_p = post.portuguese_translated_post.last()
    ru_p = post.russian_translated_post.last()
    es_p = post.spanish_translated_post.last()
    vi_p = post.vietnamese_translated_post.last()

    return render(
        request,
        'blog/post/detail.html', {
            'cn_p': cn_p,
            'hi_p': hi_p,
            'ar_p': ar_p,
            'tl_p': tl_p,
            'fr_p': fr_p,
            'de_p': de_p,
            'id_p': id_p,
            'it_p': it_p,
            'jp_p': jp_p,
            'ko_p': ko_p,
            'no_p': no_p,
            'pt_p': pt_p,
            'ru_p': ru_p,
            'es_p': es_p,
            'vi_p': vi_p
        }
    )


# def shared_or_others(request, pk):
#     post = get_object_or_404(
#         Post,
#         pk=pk
#     )
#     form = OtherEditForm(
#         data=request.POST
#     )
#     if request.method == 'POST':
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.post_id = pk
#             post.editor_id = request.user.id
#             post.save()
#             form.save_m2m()
#             return redirect(post.get_absolute_url())
#         else:
#             form = OtherEditForm()

from .models import TagNameValue
import enchant

def tags_posts_lists(request, slug):
    # cache.delete(f'tags_posts_lists-{slug}')
    tag = None
    tag = cache.get(f'tags_posts_lists-{slug}')
    # print(slug)
    d = enchant.Dict("en_US")
    if d.check(slug):
        if not tag:
            tag = get_object_or_404(
                MyCustomTag,
                slug=slug
            )
            cache.set(f'tags_posts_lists-{slug}', tag, on_day_in_seconds)
            # print(f'tags_posts_lists-{slug} not in cache')
            syn = []
            ant = []
            for synset in wordnet.synsets(tag.name):
                for idx, lemma in enumerate(synset.lemmas()):
                    syn.append(lemma.name())
                    if lemma.antonyms():
                        ant.append(lemma.antonyms()[0].name())
            set_syn = set(syn)
            set_syn.remove(tag.slug)
            # print(syn)
            # print("Set")
            suggested_tags = []
            for word in set_syn:
                try:
                    if MyCustomTag.objects.get(slug=word).slug == word:
                        # print(word, "@@@@::Exists in tags")
                        suggested_tags.append(word)
                except MyCustomTag.DoesNotExist:
                    # print(word, "####::Not")
                    pass
            for word in set(ant):
                try:
                    if MyCustomTag.objects.get(slug=word).slug == word:
                        # print(word, "@@@@::Exists in tags")
                        suggested_tags.append(word)
                except MyCustomTag.DoesNotExist:
                    # print(word, "####::Not")
                    pass
            
            try:
                first_word = wordnet.synset(f'{tag.slug}.n.01')
            except:
                try:
                    first_word = wordnet.synset(f'{tag.slug}.v.01')
                except:
                    try:
                        first_word = wordnet.synset(f'{tag.slug}.r.01')
                    except:
                        try:
                            first_word = wordnet.synset(f'{tag.slug}.a.01')
                        except:
                            first_word = wordnet.synset(f'{tag.slug}.s.01')

            sort = {}
            for word in suggested_tags:
                try:
                    second_word = wordnet.synset(f'{word}.v.01')
                    sort[word] = first_word.wup_similarity(second_word)
                except:
                    second_word = wordnet.synset(f'{word}.n.01')
                    sort[word] = first_word.wup_similarity(second_word)
                # print(first_word.wup_similarity(second_word),word)
            
            import operator
            des = sorted(sort.items(), key=operator.itemgetter(1), reverse=True)
            
            tag_items = []
            for item, key in des:
                # print(item, 'item')
                tag_items.append(item)
            
            # t_objects = Q()
            # for item in tag_items:
            #     t_objects |= Q(slug=item)
            
            # related_tags = MyCustomTag.objects.filter(t_objects)
                
            whens = []
            try:
                for sort_index, value in enumerate(tag_items):
                    whens.append(models.When(slug=value, then=sort_index))
                    qs = MyCustomTag.objects.filter(slug__in=tag_items).annotate(
                        _sort_index=models.Case(*whens, output_field=models.IntegerField())
                    )
                    # print("Here")
                
                sorted_related_tags = qs.order_by('_sort_index')[:10]
                cache.set(f'sorted_related_tags-{tag}', sorted_related_tags, on_day_in_seconds)
            except:
                sorted_related_tags = MyCustomTag.objects.all()[:10]
            


        else:
            # print(f'tags_posts_lists-{slug} get from cache')
            pass
    
    else:
        tag = get_object_or_404(
                MyCustomTag,
                slug=slug
            )

    sorted_related_tags = cache.get(f'sorted_related_tags-{tag}')


    posts = Post.aupm.all().filter(tags__slug__in=[tag.slug])
    # posts = Post.objects.all().filter(tags__slug__in=[tag.slug])
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
        print(posts)
    if request.is_ajax():
        return render(
            request,
            'account/me/fallowing/ajax_list.html',{
                'posts': posts
            }
        )
    return render(
        request,
        'account/me/fallowing/post.html', {
            'posts': posts,
            'sorted_related_tags': sorted_related_tags,
            'tag' : tag,
        }
    )


@ajax_required
@require_POST
@login_required
def tag_follow(request):
    tag_id = request.POST.get('id')
    action = request.POST.get('action')
    print(action)
    if tag_id and action:
        try:
            tag = MyCustomTag.objects.get(id=tag_id)
            if action == 'follow':
                # print("action Follow")
                TagContact.objects.get_or_create(
                    user_from=request.user,
                    to_tag=tag
                )
            else:
                # print("action Un Follow")
                TagContact.objects.filter(
                    user_from=request.user,
                    to_tag=tag
                ).delete()
            return JsonResponse({'status': 'ok'})
        except MyCustomTag.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


from translates.hindi_translate.models import HindiTranslatedPost
from translates.french_translate.models import FrenchTranslatedPost
from translates.chinese_translate.models import ChineseTranslatedPost
from translates.spanish_translate.models import SpanishTranslatedPost
from translates.arabic_translate.models import ArabicTranslatedPost
from translates.indonesian_translate.models import IndonesianTranslatedPost
from translates.portuguese_translate.models import PortugueseTranslatedPost
from translates.japanese_translate.models import JapaneseTranslatedPost
from translates.russian_translate.models import RussianTranslatedPost
from translates.german_translate.models import GermanTranslatedPost
from translates.korean_translate.models import KoreanTranslatedPost
from translates.norwegian_translate.models import NorwegianTranslatedPost
from translates.vietnamese_translate.models import VietnameseTranslatedPost
from translates.filipino_translate.models import FilipinoTranslatedPost
from translates.italian_translate.models import ItalianTranslatedPost
from translates.english_translate.models import EnglishTranslatedPost

from .forms import TranslatePostForm

@login_required
def update_translate_post(request, pk, id):
    p = get_object_or_404(Post, pk=id)
    print(p)
    language = request.LANGUAGE_CODE
    if language == 'hi':
        post = get_object_or_404(HindiTranslatedPost, pk=pk)
    elif language == 'en':
        post = get_object_or_404(EnglishTranslatedPost, pk=pk)
    elif language == 'ko':
        post = get_object_or_404(KoreanTranslatedPost, pk=pk)
    elif language == 'zh-hans':
        post = get_object_or_404(ChineseTranslatedPost, pk=pk)
    elif language == 'ar':
        post = get_object_or_404(ArabicTranslatedPost, pk=pk)
    elif language == 'ta':
        post = get_object_or_404(FilipinoTranslatedPost, pk=pk)
    elif language == 'fr':
        post = get_object_or_404(FrenchTranslatedPost, pk=pk)
    elif language == 'de':
        post = get_object_or_404(GermanTranslatedPost, pk=pk)
    elif language == 'id':
        post = get_object_or_404(IndonesianTranslatedPost, pk=pk)
    elif language == 'it':
        post = get_object_or_404(ItalianTranslatedPost, pk=pk)
    elif language == 'ja':
        post = get_object_or_404(JapaneseTranslatedPost, pk=pk)
    elif language == 'nn':
        post = get_object_or_404(NorwegianTranslatedPost, pk=pk)
    elif language == 'pt':
        post = get_object_or_404(PortugueseTranslatedPost, pk=pk)
    elif language == 'ru':
        post = get_object_or_404(RussianTranslatedPost, pk=pk)
    elif language == 'es':
        post = get_object_or_404(SpanishTranslatedPost, pk=pk)
    elif language == 'vi':
        post = get_object_or_404(VietnameseTranslatedPost, pk=pk)

    if post.cover:
        cover_image = post.cover.url
    else:
        cover_image = 'No image'
    form = TranslatePostForm(
        data=request.POST,
        files=request.FILES, instance=post
        )
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            post.edited_by.add(request.user)
            form.save_m2m()
            return redirect(p.get_absolute_url())
    else:
        form = TranslatePostForm(instance=post)
    return render(
        request,
        'blog/translate_update.html',{
            'form': form,
            'cover_image': cover_image
        }
    )

from account.models import Profile
@login_required
def set_language(request, lang=None):
    next_path = request.GET.get('next')
    translation.activate(lang)
    person = get_object_or_404(Profile, id=request.user.id)
    person.lang = lang
    person.save()
    after = next_path.split("/")[2:]
    joined_after = "/".join(after)
    return HttpResponseRedirect(f'/{joined_after}')