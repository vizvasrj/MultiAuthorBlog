# Generated by Django 3.2.5 on 2021-09-21 16:16

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IconCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
                ('icon', models.ImageField(upload_to='flag/')),
                ('code', models.CharField(max_length=10)),
            ],
        ),
    ]
