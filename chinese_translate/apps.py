from django.apps import AppConfig


class ChineseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chinese_translate'

    def ready(self):
        import chinese_translate.signals