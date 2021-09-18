from django.apps import AppConfig


class VietnameseTranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vietnamese_translate'

    def ready(self):
        import vietnamese_translate.signals