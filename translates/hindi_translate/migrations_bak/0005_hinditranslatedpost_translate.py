# Generated by Django 3.2.8 on 2021-12-04 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hindi_translate', '0004_remove_hinditranslatedpost_translates'),
    ]

    operations = [
        migrations.AddField(
            model_name='hinditranslatedpost',
            name='translate',
            field=models.BooleanField(default=True),
        ),
    ]
