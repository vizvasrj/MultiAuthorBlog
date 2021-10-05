from django.contrib import admin

# # Register your models here.
from .models import PublicationContact, Publication
admin.site.register(Publication)

admin.site.register(PublicationContact)