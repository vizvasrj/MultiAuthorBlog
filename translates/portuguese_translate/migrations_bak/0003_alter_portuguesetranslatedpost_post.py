# Generated by Django 3.2.10 on 2022-01-29 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0066_post_scrape_url'),
        ('portuguese_translate', '0002_portuguesetranslatedpost_translate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portuguesetranslatedpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portuguese_translated_post', to='blog.post'),
        ),
    ]
