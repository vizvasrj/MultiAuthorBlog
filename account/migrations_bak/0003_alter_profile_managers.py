# Generated by Django 3.2.5 on 2021-08-28 06:27

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_nav_color_profile_color'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('me', django.db.models.manager.Manager()),
            ],
        ),
    ]
