from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import json


class OptimizedDashboardCache:
    """优化后的仪表盘数据缓存"""
    
    CACHE_KEY_PREFIX = 'dashboard_'
    CACHE_TIMEOUT = 300  # 5分钟缓存
    
    @classmethod
    def get_cache_key(cls, user_id, version=None):
        """生成缓存键"""
        key = f"{cls.CACHE_KEY_PREFIX}{user_id}"
        if version:
            key = f"{key}_v{version}"
        return key
    
    @classmethod
    def get_dashboard_data(cls, user_id, fetch_func, version=1):
        """
        获取仪表盘数据（带缓存）
        
        Args:
            user_id: 用户ID
            fetch_func: 数据获取函数
            version: 缓存版本（用于数据格式变更时自动失效）
            
        Returns:
            tuple: (data, is_cached, cache_key)
        """
        cache_key = cls.get_cache_key(user_id, version)
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            try:
                data = json.loads(cached_data)
                return data, True, cache_key
            except json.JSONDecodeError:
                # 缓存数据格式错误，删除缓存
                cache.delete(cache_key)
        
        # 从数据库获取
        data = fetch_func()
        
        # 存入缓存
        try:
            cache.set(cache_key, json.dumps(data, default=str), cls.CACHE_TIMEOUT)
        except Exception:
            # 缓存设置失败不影响主流程
            pass
        
        return data, False, cache_key
    
    @classmethod
    def invalidate_cache(cls, user_id, version=None):
        """使缓存失效"""
        cache_key = cls.get_cache_key(user_id, version)
        cache.delete(cache_key)
    
    @classmethod
    def batch_invalidate(cls, user_ids, version=None):
        """批量清除缓存"""
        for user_id in user_ids:
            cls.invalidate_cache(user_id, version)
    
    @classmethod
    def get_cache_info(cls, user_id, version=None):
        """获取缓存信息"""
        cache_key = cls.get_cache_key(user_id, version)
        ttl = cache.ttl(cache_key)  # 剩余时间
        return {
            'key': cache_key,
            'ttl': ttl,
            'has_cache': cache.get(cache_key) is not None
        }