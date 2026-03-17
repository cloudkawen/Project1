from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from apps.items.models import Item, Category
from .utils import OptimizedDashboardCache
import json
import logging

logger = logging.getLogger(__name__)


class DashboardDataService:
    """仪表盘数据服务类 (剥离业务逻辑，便于复用和测试)"""
    
    @staticmethod
    def get_statistics(user, today):
        """获取统计数据"""
        items_qs = Item.objects.filter(user=user)
        categories_qs = Category.objects.filter(user=user)
        
        seven_days_ago = today - timedelta(days=7)
        week_later = today + timedelta(days=7)
        
        return {
            'total_items': items_qs.count(),
            'total_categories': categories_qs.count(),
            'recent_items': items_qs.filter(created_at__date__gte=seven_days_ago).count(),
            'expiring_items': items_qs.filter(
                expire_date__gte=today,
                expire_date__lte=week_later
            ).count(),
            'expired_items': items_qs.filter(expire_date__lt=today).count(),
            'items_without_category': items_qs.filter(category__isnull=True).count(),
            'items_without_expire_date': items_qs.filter(expire_date__isnull=True).count()
        }
    
    @staticmethod
    def get_items_by_category(user):
        """按分类统计物品"""
        # 修复反向关系名，根据你的 models.py
        # 如果 Category 有 related_name='items'，则用 'items'
        # 如果 Category 没有设置 related_name，则用 'item_set'
        categories = Category.objects.filter(user=user).annotate(
            item_count=Count('item_set')
        ).values('id', 'name', 'item_count').order_by('-item_count')
        
        return [
            {
                'id': category['id'],
                'name': category['name'],
                'value': category['item_count']
            }
            for category in categories
        ]
    
    @staticmethod
    def get_items_by_status(user, today):
        """按状态统计物品"""
        items_qs = Item.objects.filter(user=user)
        week_later = today + timedelta(days=7)
        
        normal_count = items_qs.filter(
            Q(expire_date__gte=week_later) | Q(expire_date__isnull=True)
        ).count()
        
        expiring_count = items_qs.filter(
            expire_date__gte=today,
            expire_date__lt=week_later
        ).count()
        
        expired_count = items_qs.filter(expire_date__lt=today).count()
        
        return [
            {'name': '正常', 'value': normal_count, 'color': '#67C23A'},
            {'name': '即将过期', 'value': expiring_count, 'color': '#E6A23C'},
            {'name': '已过期', 'value': expired_count, 'color': '#F56C6C'}
        ]
    
    @staticmethod
    def get_trend_data(user, days=30):
        """获取趋势数据（最近N天每天新增物品数）"""
        thirty_days_ago = timezone.now() - timedelta(days=days)
        
        daily_data = Item.objects.filter(
            user=user,
            created_at__gte=thirty_days_ago
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        result = []
        current_date = thirty_days_ago.date()
        today = timezone.now().date()
        
        data_dict = {item['date']: item['count'] for item in daily_data}
        
        while current_date <= today:
            count = data_dict.get(current_date, 0)
            result.append({
                'date': current_date.strftime('%m-%d'),
                'count': count
            })
            current_date += timedelta(days=1)
        
        return result
    
    @classmethod
    def get_all_dashboard_data(cls, user):
        """整合所有仪表盘数据（供缓存使用）"""
        today = timezone.now().date()
        
        stats = cls.get_statistics(user, today)
        charts = {
            'items_by_category': cls.get_items_by_category(user),
            'items_by_status': cls.get_items_by_status(user, today),
        }
        trend_data = cls.get_trend_data(user)
        
        # 简单获取最近活动
        recent_activities = cls.get_recent_activities(user)
        
        data = {
            'statistics': stats,
            'recent_activities': recent_activities,
            'quick_links': [
                {'title': '物品管理', 'path': '/items', 'icon': 'el-icon-shopping-bag-1', 'color': '#409EFF'},
                {'title': '分类管理', 'path': '/categories', 'icon': 'el-icon-folder', 'color': '#67C23A'},
                {'title': '用户管理', 'path': '/system/user', 'icon': 'el-icon-user', 'color': '#E6A23C'},
                {'title': '添加物品', 'path': '/items?action=add', 'icon': 'el-icon-plus', 'color': '#F56C6C'},
            ],
            'charts': charts,
            'trend_data': trend_data,
            'user_info': {
                'username': user.username,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            }
        }
        return data
    
    @staticmethod
    def get_recent_activities(user, limit=5):
        """获取最近活动"""
        activities = []
        
        # 最近添加的物品
        recent_items = Item.objects.filter(
            user=user
        ).order_by('-created_at')[:3]
        
        for item in recent_items:
            activities.append({
                'id': item.id,
                'type': 'item_added',
                'message': f'添加了新物品：{item.name}',
                'time': item.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # 最近添加的分类
        recent_categories = Category.objects.filter(
            user=user
        ).order_by('-created_at')[:2]
        
        for category in recent_categories:
            activities.append({
                'id': category.id,
                'type': 'category_added',
                'message': f'新增了分类：{category.name}',
                'time': category.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # 按时间排序
        activities.sort(key=lambda x: x['time'], reverse=True)
        return activities[:limit]


class CachedDashboardAPIView(APIView):
    """带缓存的仪表盘数据接口"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # 定义数据获取函数
            def fetch_dashboard_data():
                return DashboardDataService.get_all_dashboard_data(user)
            
            # 调用缓存
            data, is_cached, cache_key = OptimizedDashboardCache.get_dashboard_data(
                user.id, 
                fetch_dashboard_data
            )
            
            return Response({
                'code': 200,
                'data': data,
                'msg': 'success',
                'cached': is_cached,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"获取仪表盘数据失败: {e}", exc_info=True)
            
            # 返回错误信息
            return Response({
                'code': 500,
                'data': None,
                'msg': str(e),  # 返回具体错误信息
                'timestamp': timezone.now().isoformat()
            }, status=500)


class OptimizedDashboardAPIView(APIView):
    """优化后的仪表盘数据接口（无缓存版本）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            data = DashboardDataService.get_all_dashboard_data(user)
            
            return Response({
                'code': 200,
                'data': data,
                'msg': 'success',
                'cached': False,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'code': 500,
                'data': None,
                'msg': str(e)
            }, status=500)


# 向后兼容
class MockDashboardAPIView(CachedDashboardAPIView):
    """向后兼容的 MockDashboardAPIView"""
    pass


# 用于测试的简单版本
class SimpleDashboardAPIView(APIView):
    """简单仪表盘数据接口（用于调试）"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'code': 200,
            'data': {
                'statistics': {
                    'total_items': 156,
                    'total_categories': 8,
                    'recent_items': 12,
                    'expiring_items': 5,
                    'expired_items': 3
                },
                'message': '仪表盘数据加载成功'
            },
            'msg': 'success'
        })
class DebugDashboardAPIView(APIView):
    """仪表盘调试接口"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """调试模式，返回数据库查询结果"""
        from django.db import connection
        from django.core.cache import cache
        
        user = request.user
        response_data = {}
        
        try:
            # 1. 查询用户信息
            response_data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            
            # 2. 统计物品数量
            from apps.items.models import Item, Category
            
            items_count = Item.objects.filter(user=user).count()
            categories_count = Category.objects.filter(user=user).count()
            
            response_data['counts'] = {
                'items': items_count,
                'categories': categories_count
            }
            
            # 3. 获取缓存信息
            cache_key = f"dashboard_{user.id}_v1"
            cache_info = {
                'key': cache_key,
                'has_cache': cache.get(cache_key) is not None,
                'ttl': cache.ttl(cache_key)
            }
            
            response_data['cache_info'] = cache_info
            
            # 4. 获取最近的物品
            recent_items = Item.objects.filter(user=user).order_by('-created_at')[:5]
            response_data['recent_items'] = [
                {
                    'id': item.id,
                    'name': item.name,
                    'created_at': item.created_at
                }
                for item in recent_items
            ]
            
            return Response({
                'code': 200,
                'data': response_data,
                'msg': '调试信息'
            })
            
        except Exception as e:
            return Response({
                'code': 500,
                'data': None,
                'msg': str(e)
            }, status=500)
        