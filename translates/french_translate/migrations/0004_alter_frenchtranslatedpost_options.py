# Generated by Django 3.2.10 on 2022-02-27 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('french_translate', '0003_alter_frenchtranslatedpost_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='frenchtranslatedpost',
            options={'get_latest_by': ['id'], 'ordering': ['-updated']},
        ),
    ]