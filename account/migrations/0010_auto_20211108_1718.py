# Generated by Django 3.2.8 on 2021-11-08 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0009_alter_profile_my_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='about'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='full name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='my_theme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='account.theme', verbose_name='my theme'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='account/defaultprofileimage.jpg', upload_to='users/%Y/%m/%d', verbose_name='photo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]