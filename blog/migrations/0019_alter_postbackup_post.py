# Generated by Django 3.2.5 on 2021-09-08 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_postbackup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postbackup',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='post_backup', to='blog.post'),
        ),
    ]
