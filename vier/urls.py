"""vier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from vier import settings

SchemaView = get_schema_view(
    openapi.Info(
        title="VIER API",
        default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

my_urls = [
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]

urlpatterns = [
    path('api-doc/', SchemaView.with_ui('swagger', cache_timeout=None),
         name='schema-swagger-ui'),
    url(r'^admin/', admin.site.urls),
    path('api/v1/users/', include(('users.urls', 'users'), namespace='users')),
    # path('api/v1/feeds/', include(('feeds,urls', 'feeds'), namespace='feeds')),
    # path('api/v1/contests/', include(('contests.urls', 'contests'), namespace='contests')),
    # path('api/v1/notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    # path('api/v1/rewards/', include(('rewards.urls', 'rewards'), namespace='rewards')),
    path('api/v1/user_contests/', include(('user_contests.urls', 'user_contests'), namespace='user_contests'))
] + my_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
