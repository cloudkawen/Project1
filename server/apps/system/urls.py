from django.urls import path, include
from .views import TaskList, UserInfoView, UserViewSet, OrganizationViewSet, PermissionViewSet, RoleViewSet, PositionViewSet, TestView, DictTypeViewSet, DictViewSet, PTaskViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename="user")
router.register('organization', OrganizationViewSet, basename="organization")
router.register('permission', PermissionViewSet, basename="permission")
router.register('role', RoleViewSet, basename="role")
router.register('position', PositionViewSet, basename="position")
router.register('dicttype', DictTypeViewSet, basename="dicttype")
router.register('dict', DictViewSet, basename="dict")
router.register('ptask', PTaskViewSet, basename="ptask")

urlpatterns = [
    path('', include(router.urls)),
    path('task/', TaskList.as_view()),
    path('test/', TestView.as_view()),
    # ✅ 修复：确保用户信息接口路径正确
    path('user/info/', UserInfoView.as_view(), name='user_info'),
]

# 注意：这个URL会被映射到 /api/system/user/info/