from celery import shared_task

@shared_task
def print_full_name(name):
    print(name)
    return name