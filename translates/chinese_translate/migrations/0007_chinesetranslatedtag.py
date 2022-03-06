# Generated by Django 3.2.10 on 2022-02-27 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mytag', '0003_auto_20220227_2309'),
        ('chinese_translate', '0006_alter_chinesetranslatedpost_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseTranslatedTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chinese_tags', to='mytag.mycustomtag')),
            ],
        ),
    ]
