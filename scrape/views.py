from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from .serializers import HLPSerializer
from scrape.models import HealthlineParsed
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class HPPostView(ListCreateAPIView):
    queryset = HealthlineParsed.objects.all()
    serializer_class = HLPSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['url', ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
