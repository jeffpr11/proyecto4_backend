from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *


router = DefaultRouter()

router.register(r'event', EventViewSet, basename='event')
router.register(r'record', RecordViewSet, basename='record')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = router.urls

urlpatterns += [
    path('event/<int:event_id>/profiles/', ProfileViewSet.as_view({'get': 'list'}), name='profiles-by-event')
]
