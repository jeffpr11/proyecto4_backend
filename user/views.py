from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import viewsets
from .models import *
from .serializers import *

class TokenView(TokenObtainPairView):
    serializer_class = TokenPairSerializer
    
class ReTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = []
