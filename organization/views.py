
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from utils.permissions import *


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['members', 'level', 'principal_group']
    search_fields = ['name']
    permission_classes = [ListAdminOnly]


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    # permission_classes = []
