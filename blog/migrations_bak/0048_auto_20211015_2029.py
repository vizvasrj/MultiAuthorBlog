# Generated by Django 3.2.5 on 2021-10-15 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0047_auto_20211015_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('to_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_tag', to='blog.mycustomtag')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_from_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='mycustomtag',
            name='followers',
            field=models.ManyToManyField(related_name='t_following', through='blog.TagContact', to=settings.AUTH_USER_MODEL),
        ),
    ]
