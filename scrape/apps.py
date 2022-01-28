from django.apps import AppConfig


class ScrapeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrape'

    def ready(self):
        import scrape.signals