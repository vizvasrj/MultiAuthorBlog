# Generated by Django 4.0.4 on 2022-04-19 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portuguese_translate', '0002_remove_portuguesetranslatedpost_meta_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='portuguesetranslatedpost',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
