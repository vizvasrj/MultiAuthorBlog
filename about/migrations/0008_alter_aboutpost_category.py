# Generated by Django 3.2.10 on 2022-04-11 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0007_alter_aboutpost_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpost',
            name='category',
            field=models.CharField(choices=[('p', 'p'), ('a', 'a'), ('t', 't'), ('c', 'c'), ('d', 'd')], default='c', max_length=30),
        ),
    ]
