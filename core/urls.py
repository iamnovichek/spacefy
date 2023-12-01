from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from allauth import urls
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('apps.spacefy.urls')),
                  path('auth/', include('apps.userauth.urls')),
                  path('accounts/', include('allauth.urls')),
                  path("__debug__/", include("debug_toolbar.urls")),
                  # path('accounts/google/login/', CustomGoogleLoginView.as_view(), name='google')
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT
                         )
