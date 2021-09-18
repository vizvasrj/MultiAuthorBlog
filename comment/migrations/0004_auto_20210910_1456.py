# Generated by Django 3.2.5 on 2021-09-10 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('comment', '0003_auto_20210910_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='about_post',
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]