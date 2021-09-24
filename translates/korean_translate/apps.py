from django.apps import AppConfig


class KoreanTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.korean_translate'

    def ready(self):
        import translates.korean_translate.signals