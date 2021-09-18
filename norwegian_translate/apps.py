from django.apps import AppConfig


class NorwegianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'norwegian_translate'

    def ready(self):
        import norwegian_translate.signals