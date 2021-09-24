from django.apps import AppConfig


class IndonesianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.indonesian_translate'

    def ready(self):
        import translates.indonesian_translate.signals