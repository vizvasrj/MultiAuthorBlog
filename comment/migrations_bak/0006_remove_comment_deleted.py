# Generated by Django 3.2.10 on 2022-04-07 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_comment_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='deleted',
        ),
    ]
