# Generated by Django 3.2.5 on 2021-09-02 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20210902_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='shaid',
        ),
    ]