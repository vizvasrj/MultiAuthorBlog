from django.apps import AppConfig


class VietnameseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translates.vietnamese_translate'

    def ready(self):
        import translates.vietnamese_translate.signals