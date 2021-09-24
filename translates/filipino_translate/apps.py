from django.apps import AppConfig


class FilipinoTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.filipino_translate'

    def ready(self):
        import translates.filipino_translate.signals