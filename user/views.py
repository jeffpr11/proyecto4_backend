
from .models import *
from .serializers import *
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
        if self.request.user.is_staff:
            return Profile.objects.all().order_by('-date_created')
        else:
            return Profile.objects.filter(state=0).order_by('-date_created')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        #TODO: Agrego/modifico datos
        # data['extra_field'] = 'extra_value'

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        #TODO: Agrego/modifico datos
        # data['extra_field'] = 'extra_value'

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        instance = self.get_object()
        
        #TODO: Chequear que el state es correcto
        instance.state = 1
        
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
