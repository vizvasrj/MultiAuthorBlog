# Generated by Django 3.2.5 on 2021-09-15 20:18

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0022_alter_post_last_editeduser'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='JapaneseTranslatedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('body', models.TextField()),
                ('cover', models.ImageField(blank=True, null=True, upload_to='cover/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_likes', models.PositiveIntegerField(db_index=True, default=0)),
                ('audio', models.FileField(blank=True, upload_to='japanese_speech/')),
                ('bookmark_list', models.ManyToManyField(blank=True, related_name='japanese_translated_bookmark', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ManyToManyField(related_name='japanese_translate_edited_by', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='japanese_translated_post', to='blog.post')),
                ('tags', taggit_autosuggest.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('users_like', models.ManyToManyField(blank=True, related_name='japanese_translated_users_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
    ]
