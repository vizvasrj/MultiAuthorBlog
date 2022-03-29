from django.http import HttpResponse
from django.shortcuts import render
from .models import Sitemap
from django.views.decorators.gzip import gzip_page


def sitemap_list(request):
    sitemaps = Sitemap.objects.all()
    return render(
        request,
        'sitemap/list.html',{
            'sitemaps': sitemaps,
            
        },
        content_type='text/xml'
    )


@gzip_page
def sitemap_detail(request, name):
    try:
        sitemap = Sitemap.objects.get(name=name)
    except Sitemap.DoesNotExist:
        return HttpResponse("Does Not Exist")
    # return HttpResponse(sitemap.sitemap_file, content_type='text/xml', status=200)
    return HttpResponse(sitemap.get_absolute_url, headers={
        'Content-Type': 'application/gzip',
        # 'Content-Disposition': 'attachment; filename="foo.gz"',
    })