from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *


router = DefaultRouter()

router.register(r'event', EventViewSet, basename='event')
router.register(r'record', RecordViewSet, basename='record')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = router.urls

urlpatterns += [
    path('event/<int:event_id>/profiles/', ProfileViewSet.as_view({'get': 'list'}), name='profiles-by-event'),
    path('log/', EventLogViewSet.as_view({'get': 'list'}), name='events-log'),
    path('records/log/', RecordLogViewSet.as_view({'get': 'list'}), name='records-log'),
    path('comments/log/', CommentLogViewSet.as_view({'get': 'list'}), name='comments-log'),
    path('history/', get_history, name='log-for-app'),
    path('get_stats/', get_stats,  name='stats_event'),
]
