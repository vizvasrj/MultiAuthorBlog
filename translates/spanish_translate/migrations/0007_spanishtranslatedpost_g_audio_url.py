# Generated by Django 3.2.10 on 2022-03-22 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spanish_translate', '0006_auto_20220303_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='spanishtranslatedpost',
            name='g_audio_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
