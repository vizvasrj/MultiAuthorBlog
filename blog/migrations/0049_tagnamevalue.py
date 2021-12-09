# Generated by Django 3.2.5 on 2021-10-17 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0048_auto_20211015_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagNameValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='blog.mycustomtag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_tag', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]