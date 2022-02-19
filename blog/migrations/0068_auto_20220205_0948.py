# Generated by Django 3.2.10 on 2022-02-05 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0067_alter_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='t',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('trashed', 'Trashed')], default='published', max_length=10),
        ),
    ]