# Generated by Django 3.2.10 on 2022-04-18 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_profile_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='lang',
            field=models.CharField(choices=[('ar', 'عربي'), ('en', 'English'), ('zh_hans', '简体中文'), ('tl', 'Filipino'), ('fr', 'français'), ('de', 'Deutsch'), ('hi', 'हिंदी'), ('id', 'bahasa Indonesia'), ('it', 'Italiana'), ('ja', '日本'), ('ko', '한국인'), ('nn', 'Norsk'), ('pt', 'Português'), ('ru', 'русский'), ('es', 'Española'), ('vi', 'Tiếng Việt'), ('bn', 'বাংলা')], default='en', max_length=10),
        ),
    ]
