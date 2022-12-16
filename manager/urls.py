from django.contrib import admin
from django.urls import path, include
from user.views import  TokenView, ReTokenView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', ReTokenView.as_view(), name='token_refresh'),
    path('api/events/', include('event.urls')),
    path('api/organizations/', include('organization.urls')),
    path('api/user/', include('user.urls')),
]
