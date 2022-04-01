#rabbitmq-server& 
#background celery
# MultiAuthorBlog
# celery -A MultiAuthorBlog multi stop worker1
celery -A MultiAuthorBlog worker -B -l info
#celery -A MultiAuthorBlog worker -l info  -Q MultiAuthorBlog
