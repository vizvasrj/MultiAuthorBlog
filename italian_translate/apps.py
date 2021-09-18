from django.apps import AppConfig


class ItalianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'italian_translate'

    def ready(self):
        import italian_translate.signals