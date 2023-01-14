
from rest_framework import viewsets
from .models import *
from .serializers import *
from utils.permissions import *
from django_filters.rest_framework import DjangoFilterBackend


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['members']


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = []
