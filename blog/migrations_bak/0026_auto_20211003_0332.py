# Generated by Django 3.2.5 on 2021-10-02 22:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0025_publication_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='fallowing',
        ),
        migrations.AddField(
            model_name='publication',
            name='followers',
            field=models.ManyToManyField(related_name='publication_following', through='blog.PublicationContact', to=settings.AUTH_USER_MODEL),
        ),
    ]
