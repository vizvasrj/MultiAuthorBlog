from django.apps import AppConfig


class HindiTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hindi_translate'

    def ready(self):
        import hindi_translate.signals