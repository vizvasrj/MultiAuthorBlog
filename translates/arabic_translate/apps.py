from django.apps import AppConfig


class ArabicTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.arabic_translate'

    def ready(self):
        import translates.arabic_translate.signals