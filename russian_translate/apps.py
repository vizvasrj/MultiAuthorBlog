from django.apps import AppConfig


class RussianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'russian_translate'

    def ready(self):
        import russian_translate.signals