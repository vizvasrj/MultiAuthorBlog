from django.db import models
from autoslug import AutoSlugField

# Create your models here.

class IconCode(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    icon = models.ImageField(upload_to='flag/')
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code