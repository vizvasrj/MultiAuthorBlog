from django.apps import AppConfig


class ItalianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.italian_translate'

    def ready(self):
        import translates.italian_translate.signals