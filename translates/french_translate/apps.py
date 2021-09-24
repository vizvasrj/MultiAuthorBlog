from django.apps import AppConfig


class FrenchTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.french_translate'

    def ready(self):
        import translates.french_translate.signals