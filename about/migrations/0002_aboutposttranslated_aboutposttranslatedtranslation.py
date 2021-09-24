# Generated by Django 3.2.5 on 2021-09-20 22:45

from django.db import migrations, models
import django.db.models.deletion
import django_editorjs_fields.fields
import parler.fields
import parler.models
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('account', '0004_alter_profile_managers'),
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPostTranslated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='about/images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='t_about_posts', to='account.profile')),
                ('tags', taggit_autosuggest.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AboutPostTranslatedTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(db_index=True, max_length=256)),
                ('slug', models.SlugField(max_length=256)),
                ('body', django_editorjs_fields.fields.EditorJsTextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='about.aboutposttranslated')),
            ],
            options={
                'verbose_name': 'about post translated Translation',
                'db_table': 'about_aboutposttranslated_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
