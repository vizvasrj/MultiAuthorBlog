# Generated by Django 3.2.10 on 2022-04-10 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chinese_translate', '0009_chinesetranslatedpost_g_audio_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chinesetranslatedtag',
            options={'get_latest_by': ['created']},
        ),
    ]