
from .models import *
from .serializers import *
from django.db.models import Count
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status


class TokenView(TokenObtainPairView):
    serializer_class = TokenPairSerializer


class ReTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
    
    def get_queryset(self):

        countAgregate = Profile.objects.annotate(total_groups = Count('group'))

        if self.request.user.is_staff:
            return countAgregate.order_by('-date_created')
        else:
            return countAgregate.filter(state=0).order_by('-date_created')

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
