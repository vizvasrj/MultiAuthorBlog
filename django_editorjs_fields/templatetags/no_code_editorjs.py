import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def generate_paragraph(data):
    text = data.get('text').replace('&nbsp;', ' ')
    return f'{text}'


def generate_quote(data):
    caption = data.get('caption')
    text = data.get('text')

    if caption:
        caption = f'<cite>{caption}</cite>'


    return f' {text}: {caption} '


@register.filter(is_safe=True)
def no_code_editorjs(value):
    if not isinstance(value, dict):
        try:
            value = json.loads(value)
        except ValueError:
            return value
        except TypeError:
            return value

    html_list = []
    for item in value['blocks']:

        type, data = item.get('type'), item.get('data')

        if type == 'paragraph':
            html_list.append(generate_paragraph(data))
        elif type == 'Quote':
            html_list.append(generate_quote(data))

    return mark_safe(''.join(html_list))
