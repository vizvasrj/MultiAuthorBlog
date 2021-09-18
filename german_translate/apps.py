from django.apps import AppConfig


class GermanTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'german_translate'

    def ready(self):
        import german_translate.signals