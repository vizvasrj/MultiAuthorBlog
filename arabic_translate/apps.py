from django.apps import AppConfig


class ArabicTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arabic_translate'

    def ready(self):
        import arabic_translate.signals