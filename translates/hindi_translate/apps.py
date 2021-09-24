from django.apps import AppConfig


class HindiTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.hindi_translate'

    def ready(self):
        import translates.hindi_translate.signals