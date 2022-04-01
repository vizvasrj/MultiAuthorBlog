from django import template
from ..models import Post

from django.db.models import Count, query
from django.utils.safestring import mark_safe

from django.utils.html import format_html
from lxml.html.clean import (
    clean_html, Cleaner
)


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
    read = readtime.of_html(html)
    # print(read)
    read_splited = str(read).split(' ')[0]
    return read_splited

register.filter('readtime', read)


from bs4 import BeautifulSoup


def get_vimeo_id(url):
    from urllib.parse import urlparse
    query = urlparse(url)
    return query.path

def get_spotify_id(url):
    from urllib.parse import urlparse
    query = urlparse(url)
    return query.path

def get_daily_motion_video_id(url):
    from urllib.parse import urlparse, parse_qs
    
    query = urlparse(url)
    if 'dailymotion' in query.hostname:
        return (query.path).split('/')[2]
    else:
        raise ValueError



def get_yt_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube
    
    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
      
      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """

    from urllib.parse import urlparse, parse_qs

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError

def youtube(watch_id):
    return f"""
        <div style="position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;">
            <iframe src="https://www.youtube.com/embed/{watch_id}"
                style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;"
                frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
        </div>
        """

def dailymotion(watch_id):
    return f"""
        <div style="position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;">
            <iframe src="https://www.dailymotion.com/embed/video/{watch_id}"
                style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;"
                frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
            </iframe>
        </div>
        """
def soptify(long_hex_id):
    return f'''
    <iframe src="https://open.spotify.com/embed{long_hex_id}" width="100%"
     height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe> 
    '''

def vimeo(vimeo_video_id):
    return f'''
    <iframe src="https://player.vimeo.com/video{vimeo_video_id}"
     width="100%" height="360" frameborder="0" allow="autoplay; 
     fullscreen; picture-in-picture" allowfullscreen>
    </iframe>
    '''

def soups(html):
    soup = BeautifulSoup(html, 'html.parser')
    lists = []
    for x in soup:
        if x.name == 'script':
            lists.append(str(x).replace('<',"&lt;").replace('>',"&gt;"))
        if x.name == None:
            pass
        if x.name != 'script':
            if 'oembed url=' in str(x):
                # lists.append(str(x))
                pass
            else:
                lists.append(str(x))
        if x.name == 'figure':

            from urllib.parse import urlparse
            if 'https://' in str(x):
                url = str(x).split('"')[3]
            else:
                url = str(x).split('"')[2]
            query = urlparse(url)
            try:
                if 'youtu' or 'youtube' in query.hostname:
                        
                    try:
                        watch_id = get_yt_video_id(url)
                        lists.append(youtube(watch_id=watch_id))
                    except:
                        pass
                if 'daily' in query.hostname:
                    try:
                        watch_id = get_daily_motion_video_id(url)
                        # print(watch_id, "dailymotion")
                        lists.append(dailymotion(watch_id=watch_id))
                    except:
                        pass
                if 'spotify' in query.hostname:
                    try:
                        long_hex_id = get_spotify_id(url)
                        lists.append(soptify(long_hex_id=long_hex_id))
                    except:
                        pass
                if 'vimeo' in query.hostname:
                    try:
                        vimeo_video_id = get_vimeo_id(url)
                        lists.append(vimeo(vimeo_video_id=vimeo_video_id))
                    except:
                        pass
                else:
                    pass
            except:
                pass

    joined_html = ''.join(lists)

    # print(joined_html)
    return joined_html

@register.filter(is_safe=True, name='xssprotect')
def xssprotect(html):
    htmlone = soups(html)
    # print(htmlone)
    return mark_safe(htmlone)



import re

@register.filter(is_safe=True, name='removeimage')
def removeimage(html):
    string = re.sub('<a.*?>|</a> ', ' ', html)
    string2 = re.sub('<img.*?>', ' ', string)
    return string2


@register.filter
def div( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = int( value )
        arg = int( arg )
        if arg: return value / arg
    except: pass
    return ''


def paragraph_soup(html):
    # This will extract all and only  paragraphs from html
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.get_text()
    # paragraphs = []
    # for x in soup:
    #     if x.name == 'p':
    #         for y in x:
    #             if y.name == 'img':
    #                 pass
    #             else:
    #                 # encoded_html = (str(x).replace('<','&lt;').replace('>','&gt;'))
    #                 paragraphs.append(str(x))
    return ''.join(paragraphs)



@register.filter(is_safe=True, name='paragraph')
def paragraph(html):
    html = paragraph_soup(html)
    return mark_safe(html)


@register.filter(is_safe=True, name='t_url')
def t_url_paragraph(path):
    html = "/".join(path.split("/")[2:])
    # print(html)
    return html


@register.filter(is_safe=True, name='bing_clarity')
def bing_clarity(boolean):
    from django.conf import settings
    if settings.BING_CLARITY:
    
        return """<script>
            (function(c,l,a,r,i,t,y){
                c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i+"?ref=bwt";
                y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
            })(window, document, "clarity", "script", "b941ppgb9r");
            </script>
        """
    else:
        return ""