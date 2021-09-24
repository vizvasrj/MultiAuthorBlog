from django.apps import AppConfig


class SpanishTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.spanish_translate'

    def ready(self):
        import translates.spanish_translate.signals