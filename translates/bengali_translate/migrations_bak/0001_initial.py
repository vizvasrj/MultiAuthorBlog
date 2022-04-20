# Generated by Django 3.2.10 on 2022-04-18 19:15

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0080_post_meta_description'),
        ('about', '0016_auto_20220419_0008'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('mytag', '0003_auto_20220227_2309'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BengaliTranslatedTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bengali_tags', to='mytag.mycustomtag')),
            ],
            options={
                'get_latest_by': ['id'],
            },
        ),
        migrations.CreateModel(
            name='BengaliTranslatedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('body', models.TextField()),
                ('meta_description', models.CharField(blank=True, max_length=160, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='cover/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_likes', models.PositiveIntegerField(db_index=True, default=0)),
                ('audio', models.FileField(blank=True, upload_to='bengali_speech/')),
                ('translate', models.BooleanField(default=True)),
                ('audio_url', models.URLField(blank=True, null=True)),
                ('g_audio_url', models.URLField(blank=True, null=True)),
                ('bookmark_list', models.ManyToManyField(blank=True, related_name='bengali_translated_bookmark', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ManyToManyField(related_name='bengali_translate_edited_by', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bengali_translated_post', to='blog.post')),
                ('tags', taggit_autosuggest.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('users_like', models.ManyToManyField(blank=True, related_name='bengali_translated_users_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
                'get_latest_by': ['created'],
            },
        ),
        migrations.CreateModel(
            name='BengaliTranslatedAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bengali_about', to='about.aboutpost')),
            ],
            options={
                'ordering': ['-updated'],
                'get_latest_by': ['created'],
            },
        ),
    ]
