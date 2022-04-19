# Generated by Django 3.2.10 on 2022-04-18 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0016_auto_20220419_0008'),
        ('russian_translate', '0010_russiantranslatedpost_meta_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='RussianTranslatedAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='russian_about', to='about.aboutpost')),
            ],
            options={
                'ordering': ['-updated'],
                'get_latest_by': ['created'],
            },
        ),
    ]
