from django.apps import AppConfig


class JapaneseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.japanese_translate'

    def ready(self):
        import translates.japanese_translate.signals