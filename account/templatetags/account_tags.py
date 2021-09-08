from django import template
from blog.models import Post

from django.db.models import Count
from account.models import Profile

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)