from django.apps import AppConfig


class PortugueseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.portuguese_translate'

    def ready(self):
        import translates.portuguese_translate.signals