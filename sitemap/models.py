from django.db import models
from django.urls import reverse

# Every post will send post_save signel to this
# And post-update also 

# This will be updated daily and deleted on 1000 urls 
# and monthly both variable
# No 
# Sitemap model 
class ArabicUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

class ChineseUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class EnglishUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class FilipinoUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class FrenchUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class GermanUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class HindiUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class IndonesianUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class ItalianUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class JapaneseUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class KoreanUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class NorwegianUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class PortugueseUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class RussianUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class SpanishUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class VietnameseUrls(models.Model):
    slug = models.URLField(unique=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class Sitemap(models.Model):
    name = models.CharField(max_length=256, unique=True)
    sitemap_file = models.FileField(upload_to='sitemap/%d_%m_%Y/')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("sitemap_detail", kwargs={"name": self.name})
# https://www.google.com/ping?sitemap=https://example.com/sitemap.xml