# Generated by Django 3.2.10 on 2022-03-04 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_merge_20211220_2149'),
        ('publication', '0007_merge_0006_auto_20211106_0146_0006_auto_20211108_1718'),
        ('blog', '0075_auto_20220228_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='blog_posts', to='account.profile', verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cover2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='im_posts', to='blog.image', verbose_name='cover image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to='publication.publication', verbose_name='publication'),
        ),
    ]
