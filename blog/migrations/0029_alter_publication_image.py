# Generated by Django 3.2.5 on 2021-10-03 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_alter_publication_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='image',
            field=models.ImageField(null=True, upload_to='publication'),
        ),
    ]