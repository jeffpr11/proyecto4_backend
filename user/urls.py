from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()

router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = router.urls

urlpatterns += [
    path('get_stats/', get_stats,  name='stats_user'),
    path('profiles/log/', LogProfileViewSet.as_view({'get': 'list'}), name='profiles-log')
]