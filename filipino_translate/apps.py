from django.apps import AppConfig


class FilipinoTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filipino_translate'

    def ready(self):
        import filipino_translate.signals