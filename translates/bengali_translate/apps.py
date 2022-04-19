from django.apps import AppConfig


class BengaliTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.bengali_translate'

    def ready(self):
        import translates.bengali_translate.signals