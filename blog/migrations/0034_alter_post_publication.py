# Generated by Django 3.2.5 on 2021-10-04 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0002_publication_followers'),
        ('blog', '0033_alter_post_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='publication.publication'),
        ),
    ]