# Generated by Django 4.0.4 on 2022-04-19 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indonesian_translate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indonesiantranslatedpost',
            name='meta_description',
        ),
    ]
