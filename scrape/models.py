from turtle import st
from django.db import models

# Create your models here.
# this is raw scraped data 
class Healthline(models.Model):
    title = models.CharField(max_length=300)
    news_website = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, db_index=True)
    thumbnail = models.CharField(
        max_length=200, blank=True
    )
    author = models.TextField(blank=True)
    checker_runtime = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.title


# this is cleaned and parsed data
class HealthlineParsed(models.Model):
    title = models.CharField(max_length=200)
    news_website = models.CharField(
        max_length=3,
        blank=True,
        null=True
    )
    original_date = models.DateField(
        blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, db_index=True, unique=True)
    thumbnail = models.CharField(
        max_length=200, blank=True
    )
    author = models.TextField(
        blank=True, null=True
    )
    checker_runtime = models.CharField(
        max_length=20,
        blank=True, null=True
    )
    def __str__(self):
        return self.title


# this is data thats direct need to be translation
# also this data will be in chunks of data
class HealthlineChunksNumber(models.Model):
    url = models.CharField(max_length=300)
    def __str__(self):
        num = HealthlineChunksNumber.objects.get(id=self.id)
        count = num.chunks.all().count()
        return f'{self.url}__total: {count}' 
    

class HealthlineChunks(models.Model):
    url = models.ForeignKey(
        HealthlineChunksNumber,
        on_delete=models.CASCADE,
        related_name='chunks'
    )
    data_chunk = models.TextField()
    def __str__(self):
        return self.data_chunk[1:50]
