from celery import shared_task
from publication.models import Publication as Pub
@shared_task
def add_admin_to_publication(pk):
    import time
    time.sleep(2)
    pub = Pub.objects.get(id=pk)
    pub.content_creater.add(pub.publisher)
    return True