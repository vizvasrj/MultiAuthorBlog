# Generated by Django 3.2.10 on 2022-03-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korean_translate', '0005_koreantranslatedtag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='koreantranslatedpost',
            options={'get_latest_by': ['created'], 'ordering': ['-updated']},
        ),
        migrations.AddField(
            model_name='koreantranslatedpost',
            name='audio_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
