# Generated by Django 3.2.8 on 2021-12-03 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinese_translate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chinesetranslatedpost',
            name='translate',
            field=models.BooleanField(default=True),
        ),
    ]
