from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'group', GroupViewSet, basename='event')
router.register(r'resource', ResourceViewSet, basename='record')

urlpatterns = router.urls
