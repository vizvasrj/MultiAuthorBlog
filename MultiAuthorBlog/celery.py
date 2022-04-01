import os
from celery import Celery
from celery.schedules import crontab
from sitemap.tasks import sitemap_creator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MultiAuthorBlog.settings')
app = Celery("MultiAuthorBlog")
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# This function will call every day one o clock
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        crontab(minute=0, hour=1), 
        daily_sitemap_generate.s(),
    )

@app.task
def daily_sitemap_generate():
    print("EVER MINUTE")
    sitemap_creator()
