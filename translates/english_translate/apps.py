from django.apps import AppConfig


class EnglishTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.english_translate'

    def ready(self):
        import translates.english_translate.signals