from django.apps import AppConfig


class ChineseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.chinese_translate'

    def ready(self):
        import translates.chinese_translate.signals