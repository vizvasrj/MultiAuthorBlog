# Generated by Django 3.2.8 on 2021-12-04 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hindi_translate', '0003_rename_translate_hinditranslatedpost_translates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hinditranslatedpost',
            name='translates',
        ),
    ]