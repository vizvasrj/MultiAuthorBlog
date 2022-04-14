from django import template

register = template.Library()

@register.filter(is_safe=True, name='tem_tags')
def tem_tags(post, language):
    # from termcolor import colored
    # print(colored(post, 'yellow'))
    # print(colored(language, 'magenta'))
    from blog.tblog.utils import get_tpost_ttags
    t_tags = get_tpost_ttags(is_post=post, need_tags=True, language=language)
    return t_tags


@register.filter(is_safe=True, name='tr_post')
def tr_post(post, language):
    from blog.tblog.utils import get_tpost_ttags
    t_post = get_tpost_ttags(is_post=post, language=language, need_post=True)
    return t_post


@register.filter(is_safe=True, name='short')
def short(body, ln):
    if ln in ('ko', 'ja', 'zh-hans'):
        body = body[:100]
    else:
        body = ' '.join(body.split(' ')[:100])
    return body