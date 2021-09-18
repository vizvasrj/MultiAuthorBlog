from django.apps import AppConfig


class SpanishTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spanish_translate'

    def ready(self):
        import spanish_translate.signals