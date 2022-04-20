# Generated by Django 3.2.5 on 2021-10-15 06:40

from django.db import migrations
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0040_auto_20211015_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topics',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='ArticleTopic',
        ),
        migrations.DeleteModel(
            name='Topics',
        ),
    ]
