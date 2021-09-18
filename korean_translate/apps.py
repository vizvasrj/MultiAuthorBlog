from django.apps import AppConfig


class KoreanTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'korean_translate'

    def ready(self):
        import korean_translate.signals