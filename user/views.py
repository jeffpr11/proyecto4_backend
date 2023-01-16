
from .models import *
from .serializers import *
from django.db.models import Count
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class TokenView(TokenObtainPairView):
    serializer_class = TokenPairSerializer
    
class ReTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']

    def get_queryset(self):
        return Profile.objects.annotate(
            total_groups = Count('group')
        )
