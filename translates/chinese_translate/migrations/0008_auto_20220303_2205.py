# Generated by Django 3.2.10 on 2022-03-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinese_translate', '0007_chinesetranslatedtag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chinesetranslatedpost',
            options={'get_latest_by': ['created'], 'ordering': ['-updated']},
        ),
        migrations.AddField(
            model_name='chinesetranslatedpost',
            name='audio_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]