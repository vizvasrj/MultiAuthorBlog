# You will need to set initial counts for the rest of the Post objects to match the
# current status of the database. Open the shell with the python manage.py shell


from blog.models import Post
for post in Post.objects.all():
    post.total_likes = post.users_like.count()
    post.save()
