
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from utils.permissions import *


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['members', 'level', 'principal_group']
    search_fields = ['name']
    permission_classes = [ListAdminOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Group.objects.all().order_by('-date_created')
        else:
            return Group.objects.filter(state=0).order_by('-date_created')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        username = request.user.get_full_name()[:30]
        data['user_creator'] = username
        data['user_modifier'] = username
        data['state'] = 0
        data['last_action'] = 0

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        if request.GET.get('members_recursive', None):
            queryset = instance.get_related_members()
        if request.GET.get('leaders_recursive', None):
            queryset = instance.get_related_leaders()
        if bool(request.GET):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serialized = ProfileSerializer(page, many=True)
                return self.get_paginated_response(serialized.data)
        serialized = self.serializer_class(instance)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        username = request.user.get_full_name()[:30]
        data['user_modifier'] = username
        data['last_action'] = 1

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()

        username = request.user.get_full_name()[:30]
        instance.user_modifier = username
        instance.state = 1
        instance.last_action = 2
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Resource.objects.all().order_by('-date_created')
        else:
            return Resource.objects.filter(state=0).order_by('-date_created')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        username = request.user.get_full_name()[:30]
        data['user_creator'] = username
        data['user_modifier'] = username
        data['state'] = 0
        data['last_action'] = 0

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        username = request.user.get_full_name()[:30]
        data['user_modifier'] = username
        data['last_action'] = 1

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()

        username = request.user.get_full_name()[:30]
        instance.user_modifier = username
        instance.state = 1
        instance.last_action = 2
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
