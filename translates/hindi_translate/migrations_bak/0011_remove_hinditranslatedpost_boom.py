# Generated by Django 3.2.8 on 2021-12-04 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hindi_translate', '0010_hinditranslatedpost_boom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hinditranslatedpost',
            name='boom',
        ),
    ]
