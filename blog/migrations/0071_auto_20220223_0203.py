# Generated by Django 3.2.10 on 2022-02-22 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0070_alter_post_t'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='cover/%Y/%m/%d', verbose_name='cover')),
                ('creator_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='photographer name')),
                ('creator_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='photographer profile url')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='cover2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='im_posts', to='blog.image', verbose_name='cover image'),
        ),
    ]