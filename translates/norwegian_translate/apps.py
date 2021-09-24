from django.apps import AppConfig


class NorwegianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.norwegian_translate'

    def ready(self):
        import translates.norwegian_translate.signals