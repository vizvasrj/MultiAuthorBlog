from celery import shared_task
from publication.models import Publication
@shared_task
def add_admin_to_publication(pk):
    import time
    time.sleep(2)
    pub = Publication.objects.get(id=pk)
    publisher = pub.publisher
    if publisher in pub.writer.all():
        pub.writer.remove(publisher)

    return True