from django.contrib.sitemaps import Sitemap

from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    protocol = 'https'
    # limit = 5
    languages = [x for x in ['hi', 'en']]
    i18n = True

    def items(self):
        return Post.aupm.all()
    
    def lastmod(self, obj):
        return obj.updated
