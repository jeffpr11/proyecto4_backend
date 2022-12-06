from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'event', EventViewSet, basename='event')
router.register(r'record', RecordViewSet, basename='record')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = router.urls
