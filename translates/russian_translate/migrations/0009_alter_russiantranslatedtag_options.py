# Generated by Django 3.2.10 on 2022-04-10 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('russian_translate', '0008_alter_russiantranslatedtag_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='russiantranslatedtag',
            options={'get_latest_by': ['id']},
        ),
    ]