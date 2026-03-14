from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Count, Q, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, serializers, filters, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item, Category


# =====================
# Serializer
# =====================

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    item_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ["id", "name", "item_count", "created_at"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        """创建分类时自动关联当前用户"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ItemSerializer(serializers.ModelSerializer):
    """物品序列化器"""
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    
    status = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)
    days_to_expire = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "category",
            "category_name",
            "location",
            "expire_date",
            "status",
            "days_to_expire",
            "user_name",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["user", "created_at", "updated_at"]
    
    def get_status(self, obj):
        """计算物品状态"""
        if not obj.expire_date:
            return "normal"
        
        today = timezone.now().date()
        
        if obj.expire_date < today:
            return "expired"
        elif obj.expire_date <= today + timedelta(days=7):
            return "expiring"
        else:
            return "normal"
    
    def get_days_to_expire(self, obj):
        """计算距离过期天数"""
        if not obj.expire_date:
            return None
        
        today = timezone.now().date()
        if obj.expire_date >= today:
            return (obj.expire_date - today).days
        return -1  # 已过期
    
    def create(self, validated_data):
        """创建物品时自动关联当前用户"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """更新物品时保留原有用户"""
        validated_data.pop('user', None)  # 防止用户被修改
        return super().update(instance, validated_data)


# =====================
# 分类管理
# =====================

class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        """只返回当前用户的分类"""
        return Category.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """删除分类前检查是否有物品使用"""
        instance = self.get_object()
        
        # 检查分类下是否有物品
        if instance.items.exists():
            return Response(
                {"detail": "该分类下存在物品，无法删除"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)


# =====================
# 物品管理
# =====================

class ItemViewSet(viewsets.ModelViewSet):
    """物品视图集"""
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # 配置过滤、搜索、排序
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'expire_date': ['gte', 'lte', 'exact'],
        'location': ['exact', 'icontains'],
    }
    search_fields = ['name', 'location', 'category__name']
    ordering_fields = ['name', 'expire_date', 'created_at', 'updated_at']
    ordering = ['-created_at']  # 默认按创建时间倒序
    
    def get_queryset(self):
        """只返回当前用户的物品，支持状态过滤"""
        queryset = Item.objects.filter(user=self.request.user)
        
        # 处理状态过滤
        status_param = self.request.query_params.get('status', None)
        if status_param:
            today = timezone.now().date()
            
            if status_param == 'expired':
                queryset = queryset.filter(expire_date__lt=today)
            elif status_param == 'expiring':
                queryset = queryset.filter(
                    expire_date__gte=today,
                    expire_date__lte=today + timedelta(days=7)
                )
            elif status_param == 'normal':
                queryset = queryset.filter(
                    Q(expire_date__gt=today + timedelta(days=7)) |
                    Q(expire_date__isnull=True)
                )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取物品统计信息"""
        user = request.user
        today = timezone.now().date()
        
        # 总物品数
        total_items = Item.objects.filter(user=user).count()
        
        # 过期统计
        expired_items = Item.objects.filter(
            user=user,
            expire_date__lt=today
        ).count()
        
        expiring_items = Item.objects.filter(
            user=user,
            expire_date__gte=today,
            expire_date__lte=today + timedelta(days=7)
        ).count()
        
        # 分类统计
        category_stats = Category.objects.filter(user=user).annotate(
            item_count=Count('items')
        ).filter(item_count__gt=0).values('name', 'item_count')
        
        # 位置统计
        location_stats = Item.objects.filter(
            user=user
        ).exclude(location__isnull=True).exclude(location='').values(
            'location'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # 过期趋势（最近7天）
        trend_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            count = Item.objects.filter(
                user=user,
                expire_date=date
            ).count()
            trend_data.append({
                "date": date.strftime("%m-%d"),
                "count": count
            })
        
        # 即将过期的物品
        upcoming_expires = Item.objects.filter(
            user=user,
            expire_date__gte=today,
            expire_date__lte=today + timedelta(days=3)
        ).order_by('expire_date')[:5]
        
        upcoming_expires_data = []
        for item in upcoming_expires:
            days_left = (item.expire_date - today).days
            upcoming_expires_data.append({
                "id": item.id,
                "name": item.name,
                "expire_date": item.expire_date,
                "days_left": days_left,
                "category": item.category.name if item.category else None
            })
        
        return Response({
            "total_items": total_items,
            "expired_items": expired_items,
            "expiring_items": expiring_items,
            "normal_items": total_items - expired_items - expiring_items,
            
            "category_stats": list(category_stats),
            "location_stats": list(location_stats),
            "expire_trend": trend_data,
            "upcoming_expires": upcoming_expires_data
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """获取物品概览（用于Dashboard）"""
        user = request.user
        today = timezone.now().date()
        
        # 获取物品总数
        total_items = Item.objects.filter(user=user).count()
        
        # 已过期物品
        expired_items = Item.objects.filter(
            user=user,
            expire_date__lt=today
        ).count()
        
        # 即将过期（7天内）
        expiring_items = Item.objects.filter(
            user=user,
            expire_date__gte=today,
            expire_date__lte=today + timedelta(days=7)
        ).count()
        
        # 正常物品
        normal_items = Item.objects.filter(
            user=user
        ).filter(
            Q(expire_date__gt=today + timedelta(days=7)) |
            Q(expire_date__isnull=True)
        ).count()
        
        return Response({
            "total": total_items,
            "expired": expired_items,
            "expiring": expiring_items,
            "normal": normal_items
        })


# =====================
# Dashboard 数据
# =====================

class DashboardOverview(APIView):
    """Dashboard数据接口"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # 基础统计
        total_items = Item.objects.filter(user=user).count()
        expired_items = Item.objects.filter(
            user=user,
            expire_date__lt=today
        ).count()
        expiring_items = Item.objects.filter(
            user=user,
            expire_date__gte=today,
            expire_date__lte=today + timedelta(days=7)
        ).count()

        # 分类统计（包含具体数据）
        category_stats = Category.objects.filter(user=user).annotate(
            total=Count('items')
        ).filter(total__gt=0).values('id', 'name', 'total').order_by('-total')

        # 按位置统计
        location_stats = Item.objects.filter(
            user=user
        ).exclude(location__isnull=True).exclude(location='').values(
            'location'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        # 过期趋势（最近7天）
        trend = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            count = Item.objects.filter(
                user=user,
                expire_date=day
            ).count()
            trend.append({
                "date": day.strftime("%m-%d"),
                "count": count
            })

        # 最近添加的物品
        recent_items = Item.objects.filter(
            user=user
        ).order_by("-created_at")[:5]

        # 即将过期的物品
        upcoming_expires = Item.objects.filter(
            user=user,
            expire_date__gte=today,
            expire_date__lte=today + timedelta(days=3)
        ).order_by('expire_date')[:5]

        return Response({
            "stats": {
                "total_items": total_items,
                "expired_items": expired_items,
                "expiring_items": expiring_items,
                "normal_items": total_items - expired_items - expiring_items
            },
            
            "category_stats": [
                {
                    "id": c["id"],
                    "name": c["name"],
                    "value": c["total"]
                }
                for c in category_stats
            ],
            
            "location_stats": list(location_stats),
            
            "expire_trend": trend,
            
            "recent_items": [
                {
                    "id": r.id,
                    "name": r.name,
                    "category": r.category.name if r.category else "未分类",
                    "location": r.location or "",
                    "expire_date": r.expire_date,
                    "status": "expired" if r.expire_date and r.expire_date < today else
                              "expiring" if r.expire_date and r.expire_date <= today + timedelta(days=7) else
                              "normal"
                }
                for r in recent_items
            ],
            
            "upcoming_expires": [
                {
                    "id": r.id,
                    "name": r.name,
                    "category": r.category.name if r.category else "未分类",
                    "expire_date": r.expire_date,
                    "days_left": (r.expire_date - today).days
                }
                for r in upcoming_expires
            ]
        })


# =====================
# 文件管理相关
# =====================

class FileStatsView(APIView):
    """文件统计视图（如果系统有文件功能）"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # 这里可以添加文件相关的统计
        # 例如：文件总数、按类型统计等
        return Response({
            "file_count": 0,
            "total_size": 0,
            "by_type": []
        })