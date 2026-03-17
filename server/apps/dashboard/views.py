# server/apps/dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from apps.items.models import Item, Category
import datetime

class DashboardAPIView(APIView):
    """仪表盘数据接口"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # 获取统计数据
            total_items = Item.objects.filter(user=user).count()
            total_categories = Category.objects.filter(user=user).count()
            
            # 最近7天新增物品
            seven_days_ago = datetime.date.today() - datetime.timedelta(days=7)
            recent_items = Item.objects.filter(
                user=user, 
                created_at__gte=seven_days_ago
            ).count()
            
            # 即将过期物品（7天内）
            today = datetime.date.today()
            week_later = today + datetime.timedelta(days=7)
            expiring_items = Item.objects.filter(
                user=user,
                expire_date__gte=today,
                expire_date__lte=week_later
            ).count()
            
            # 已过期物品
            expired_items = Item.objects.filter(
                user=user,
                expire_date__lt=today
            ).count()
            
            # 最近活动
            recent_activities = [
                {
                    'id': 1,
                    'type': 'item_added',
                    'message': '添加了新物品：笔记本电脑',
                    'time': '2024-03-14 10:30:00'
                },
                {
                    'id': 2,
                    'type': 'item_updated',
                    'message': '更新了物品：办公椅',
                    'time': '2024-03-13 15:20:00'
                }
            ]
            
            data = {
                'statistics': {
                    'total_items': total_items,
                    'total_categories': total_categories,
                    'recent_items': recent_items,
                    'expiring_items': expiring_items,
                    'expired_items': expired_items
                },
                'recent_activities': recent_activities,
                'quick_links': [
                    {'title': '物品管理', 'path': '/items', 'icon': 'el-icon-shopping'},
                    {'title': '分类管理', 'path': '/categories', 'icon': 'el-icon-folder'},
                    {'title': '用户管理', 'path': '/system/user', 'icon': 'el-icon-user'},
                    {'title': '添加物品', 'path': '/items?action=add', 'icon': 'el-icon-plus'}
                ],
                'charts': {
                    'items_by_category': self.get_items_by_category(user),
                    'items_by_status': self.get_items_by_status(user)
                }
            }
            
            return Response({
                'code': 200,
                'data': data,
                'msg': 'success'
            })
            
        except Exception as e:
            return Response({
                'code': 500,
                'data': None,
                'msg': str(e)
            }, status=500)
    
    def get_items_by_category(self, user):
        """按分类统计物品"""
        categories = Category.objects.filter(user=user)
        data = []
        
        for category in categories:
            count = Item.objects.filter(user=user, category=category).count()
            if count > 0:
                data.append({
                    'name': category.name,
                    'value': count
                })
        
        return data
    
    def get_items_by_status(self, user):
        """按状态统计物品"""
        today = datetime.date.today()
        week_later = today + datetime.timedelta(days=7)
        
        # 正常
        normal_items = Item.objects.filter(
            user=user,
            expire_date__isnull=True
        ).count()
        
        # 即将过期
        expiring_items = Item.objects.filter(
            user=user,
            expire_date__gte=today,
            expire_date__lte=week_later
        ).count()
        
        # 已过期
        expired_items = Item.objects.filter(
            user=user,
            expire_date__lt=today
        ).count()
        
        return [
            {'name': '正常', 'value': normal_items},
            {'name': '即将过期', 'value': expiring_items},
            {'name': '已过期', 'value': expired_items}
        ]


# 如果没有模型，使用模拟数据
class MockDashboardAPIView(APIView):
    """模拟仪表盘数据接口（用于测试）"""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data = {
            'statistics': {
                'total_items': 156,
                'total_categories': 8,
                'recent_items': 12,
                'expiring_items': 5,
                'expired_items': 3
            },
            'recent_activities': [
                {
                    'id': 1,
                    'type': 'item_added',
                    'message': '添加了新物品：笔记本电脑',
                    'time': '2024-03-14 10:30:00'
                },
                {
                    'id': 2,
                    'type': 'item_updated',
                    'message': '更新了物品：办公椅',
                    'time': '2024-03-13 15:20:00'
                },
                {
                    'id': 3,
                    'type': 'category_added',
                    'message': '新增分类：电子产品',
                    'time': '2024-03-12 09:15:00'
                }
            ],
            'quick_links': [
                {'title': '物品管理', 'path': '/items', 'icon': 'el-icon-shopping'},
                {'title': '分类管理', 'path': '/categories', 'icon': 'el-icon-folder'},
                {'title': '用户管理', 'path': '/system/user', 'icon': 'el-icon-user'},
                {'title': '添加物品', 'path': '/items?action=add', 'icon': 'el-icon-plus'}
            ],
            'charts': {
                'items_by_category': [
                    {'name': '电子产品', 'value': 45},
                    {'name': '家具', 'value': 32},
                    {'name': '办公用品', 'value': 28},
                    {'name': '图书', 'value': 25},
                    {'name': '其他', 'value': 26}
                ],
                'items_by_status': [
                    {'name': '正常', 'value': 120},
                    {'name': '即将过期', 'value': 5},
                    {'name': '已过期', 'value': 3}
                ]
            }
        }
        
        return Response({
            'code': 200,
            'data': data,
            'msg': 'success'
        })
    