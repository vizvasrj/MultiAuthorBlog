from django.apps import AppConfig


class JapaneseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'japanese_translate'

    def ready(self):
        import japanese_translate.signals