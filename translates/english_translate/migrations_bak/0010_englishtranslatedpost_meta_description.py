# Generated by Django 3.2.10 on 2022-04-17 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english_translate', '0009_alter_englishtranslatedtag_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='englishtranslatedpost',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]
