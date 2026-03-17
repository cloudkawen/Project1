# server/apps/items/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "item_category"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="物品名称")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    expire_date = models.DateField(db_index=True, null=True, blank=True)  # 允许为空
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # ✅ 添加更新时间字段
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "item_info"
        ordering = ['-created_at']

    def __str__(self):
        return self.name