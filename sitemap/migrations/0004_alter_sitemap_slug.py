# Generated by Django 3.2.10 on 2022-03-28 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitemap', '0003_rename_name_sitemap_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemap',
            name='slug',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
