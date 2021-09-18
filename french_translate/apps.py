from django.apps import AppConfig


class FrenchTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'french_translate'

    def ready(self):
        import french_translate.signals