from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count
from .models import *
from .serializers import *
from user.models import Profile
from user.serializers import ProfileSerializer
from rest_framework.decorators import api_view

class EventViewSet(viewsets.ModelViewSet):
    
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        
        qs_count = Event.objects.annotate(
            total_records = Count('record', distinct=True), 
            total_comments = Count('comment', distinct=True)
        )
        
        if self.request.user.is_staff:
            return qs_count.order_by('-date_created')
        else:
            return qs_count.filter(state=0).order_by('-date_created')

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


class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Record.objects.all().order_by('-date_created')
        else:
            return Record.objects.filter(state=0).order_by('-date_created')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        username = request.user.get_full_name()[:30]
        data['user_creator'] = username
        data['user_modifier'] = username
        data['state'] = 0
        data['last_action'] = 0

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        tmp = Record.objects.filter(event=data['event'], user=data['user'])
        if tmp.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all().order_by('-date_created')
        else:
            return Comment.objects.filter(state=0).order_by('-date_created')

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


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Profile.objects.filter(record__event_id=event_id)


class EventLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.history.all()
    serializer_class = EventHistorySerializer


class RecordLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Record.history.all()
    serializer_class = RecordHistorySerializer


class CommentLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.history.all()
    serializer_class = CommentHistorySerializer


@api_view(['GET'])
def get_history(request):
    m = request.GET.get('member')
    t3 = Record.objects.filter(user=m).order_by('-date_created')
    serializer3 = RecordSerializer(t3, many=True)
    return Response({'3': serializer3.data.copy()})


@api_view(['GET'])
def get_stats(request):
    
    resp = {
        'events_count': Event.objects.filter(state=0).count(),
        'records_insterested_count': Record.objects.filter(state=0, interested_record=True, confirmed_record=False).count(),
        'records_confirmed_count': Record.objects.filter(state=0, interested_record=True, confirmed_record=True).count(),
    }
    return Response(resp)
