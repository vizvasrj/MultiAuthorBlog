from django import template
from ..models import Post

from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown
import readtime

from account.models import Profile

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('blog/post/most_commented_posts.html')
def show_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(
                                total_comments=Count('comments')  
                                ).order_by('-total_comments')[:count]
    return {'most_commented_posts': most_commented_posts}

@register.inclusion_tag('blog/post/most_liked_posts.html')
def show_most_liked_posts(count=5):
    most_liked_posts = Post.published.order_by('-total_likes')[:count]
    return {'most_liked_posts': most_liked_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments=Count('comments')
                ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

def read(html):
    return readtime.of_html(html)

register.filter('readtime', read)