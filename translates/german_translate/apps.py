from django.apps import AppConfig


class GermanTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.german_translate'

    def ready(self):
        import translates.german_translate.signals