# Generated by Django 3.2.5 on 2021-08-24 21:37

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0005_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='post_tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]