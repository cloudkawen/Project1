"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#Projects\django-vue-admin\server\server\urls.py
from apps.system.views import FileViewSet, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from django.views.generic import TemplateView
from apps.dashboard.views import CachedDashboardAPIView, MockDashboardAPIView, OptimizedDashboardAPIView, SimpleDashboardAPIView


router = routers.DefaultRouter()
router.register('', FileViewSet, basename="file")

schema_view = get_schema_view(
   openapi.Info(
      title="Django-Vue-Admin API",
      default_version='v1',
      contact=openapi.Contact(email="caoqianming@foxmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[],
)

urlpatterns = [
    path('django/admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/black/', LogoutView.as_view(), name='token_black'),
    path('api/file/', include(router.urls)),
    path('api/system/', include('apps.system.urls')),
    path('api/monitor/', include('apps.monitor.urls')),
    path('api/wf/', include('apps.wf.urls')),
    path('api/', include('apps.items.urls')),
    # 仪表盘接口
    # 主仪表盘接口（带缓存）
    path('', CachedDashboardAPIView.as_view(), name='dashboard'),
    
    # 无缓存版本（用于测试）
    path('no-cache/', OptimizedDashboardAPIView.as_view(), name='dashboard-no-cache'),
    
    # 向后兼容版本
    path('mock/', MockDashboardAPIView.as_view(), name='dashboard-mock'),
    
    # 简单测试版本
    path('simple/', SimpleDashboardAPIView.as_view(), name='dashboard-simple'),
    
    # api文档
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # 前端页面入口
    path('',TemplateView.as_view(template_name="index.html"))
] + \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
