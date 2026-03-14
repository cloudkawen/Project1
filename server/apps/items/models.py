from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "item_category"

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="物品名称")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    expire_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "item_info"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
