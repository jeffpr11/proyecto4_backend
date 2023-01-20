from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'group', GroupViewSet, basename='group')
router.register(r'resource', ResourceViewSet, basename='resource')
router.register(r'image', ImageViewSet, basename='image')

urlpatterns = router.urls
