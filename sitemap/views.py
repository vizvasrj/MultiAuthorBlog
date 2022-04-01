from django.http import HttpResponse
from django.shortcuts import render
from .models import Sitemap
from django.conf import settings


def sitemap_list(request):
    sitemaps = Sitemap.objects.all()
    return render(
        request,
        'sitemap/list.html',{
            'sitemaps': sitemaps,
            'domain': settings.HOME_DOMAIN
        },
        content_type='text/xml'
    )


def sitemap_detail(request, name):
    try:
        sitemap = Sitemap.objects.get(name=name)
    except Sitemap.DoesNotExist:
        return HttpResponse("Does Not Exist")
    return HttpResponse(sitemap.sitemap_file, content_type='text/xml', status=200)
    # return HttpResponse(sitemap.sitemap_file, headers={
    #     'Content-Type': 'application/gzip',
    #     # 'Content-Disposition': 'attachment; filename="foo.gz"',
    # })


def robots_txt(request):
    with open('sitemap/robots.txt', 'r') as f:
        text = f.read()

    return HttpResponse(text, content_type='text/plain', status=200)

