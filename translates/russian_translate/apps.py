from django.apps import AppConfig


class RussianTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.russian_translate'

    def ready(self):
        import translates.russian_translate.signals