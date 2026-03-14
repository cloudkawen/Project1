from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, 
    ItemViewSet, 
    DashboardOverview,
    FileStatsView
)


router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardOverview.as_view(), name='dashboard'),
    path('files/stats/', FileStatsView.as_view(), name='file-stats'),
    
    # 物品相关统计接口
    path('items/stats/', ItemViewSet.as_view({'get': 'stats'}), name='items-stats'),
    path('items/summary/', ItemViewSet.as_view({'get': 'summary'}), name='items-summary'),
]
