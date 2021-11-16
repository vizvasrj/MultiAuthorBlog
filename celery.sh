#rabbitmq-server& 
#background celery
# MultiAuthorBlog
# celery -A MultiAuthorBlog multi stop worker1
celery -A MultiAuthorBlog worker -l info
