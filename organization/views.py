
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from utils.permissions import *

from rest_framework.decorators import action, api_view


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = [
        'level',
        'members',
        'group_leader',
        'group_leader__user__username',
        'principal_group'
    ]

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
    
    @action(detail=False, methods=['get'])
    def member_count(self, request):
        groups = Group.objects.all()
        data = []
        for group in groups:
            active_members = group.members.filter(state=0).count()
            inactive_members = group.members.filter(state=1).count()
            data.append({
                'group': group.name,
                'active_members': active_members,
                'inactive_members': inactive_members
            })
        return Response(data)


class ResourceViewSet(viewsets.ModelViewSet):

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['groups', 'state']
    search_fields = ['name']

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


class LogGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.history.all()
    serializer_class = GroupHistorySerializer


class LogResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.history.all()
    serializer_class = ResourceHistorySerializer


@api_view(['GET'])
def get_history(request):
    m = request.GET.get('member')
    g = request.GET.get('group')
    t1 = Group.objects.prefetch_related('members').filter(members=m).first()
    t2 = Resource.objects.filter(groups=g).order_by('-date_created')
    serializer1 = GroupSerializer(t1)
    serializer2 = ResourceSerializer(t2, many=True)
    resp = {
        '1': serializer1.data.copy(),
        '2': serializer2.data.copy(),
    }
    return Response(resp)


@api_view(['GET'])
def get_stats(request):
    resp = {
        'groups_count': Group.objects.filter(state=0).count(),
        'resources_count': Resource.objects.filter(state=0).count(),
    }
    return Response(resp)
