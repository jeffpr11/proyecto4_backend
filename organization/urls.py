
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()

router.register(r'group', GroupViewSet, basename='group')
router.register(r'resource', ResourceViewSet, basename='resource')

urlpatterns = router.urls

urlpatterns += [
    path('history/', get_history, name='log-for-app'),
    path('get_stats/', get_stats,  name='stats_organization'),
    path('groups/log/', LogGroupViewSet.as_view({'get': 'list'}), name='groups-log'),
    path('resources/log/', LogResourceViewSet.as_view({'get': 'list'}), name='resources-log'),
]
