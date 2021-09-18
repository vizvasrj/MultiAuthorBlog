from django.apps import AppConfig


class IndonesianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indonesian_translate'

    def ready(self):
        import indonesian_translate.signals