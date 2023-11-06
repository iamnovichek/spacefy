from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.spacefy.urls')),
    path('auth/', include('apps.userauth.urls')),
]
