# Generated by Django 3.2.10 on 2022-04-18 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0015_auto_20220418_2349'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.RemoveField(
            model_name='aboutpost',
            name='language',
        ),
    ]