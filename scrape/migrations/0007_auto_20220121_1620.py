# Generated by Django 3.2.10 on 2022-01-21 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0006_healthlinechunks_healthlinechunksnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthlinechunks',
            name='title',
        ),
        migrations.RemoveField(
            model_name='healthlinechunksnumber',
            name='title',
        ),
        migrations.AddField(
            model_name='healthlinechunks',
            name='url',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chunks', to='scrape.healthlinechunksnumber'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='healthlinechunksnumber',
            name='url',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
