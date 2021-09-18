from django.apps import AppConfig


class PortugueseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portuguese_translate'

    def ready(self):
        import portuguese_translate.signals