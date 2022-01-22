from django.contrib import admin

# Register your models here.
from .models import (
    Healthline, 
    HealthlineChunks, 
    HealthlineParsed,
    HealthlineChunksNumber, 
    )
admin.site.register(Healthline)
admin.site.register(HealthlineParsed)
admin.site.register(HealthlineChunks)
admin.site.register(HealthlineChunksNumber)
