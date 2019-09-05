from django.db import models

# from apis.models import App


class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True)  # open_id是一个长度为32的字符串

    # 通过db_index=True把nickname定义为被索引的字段
    nickname = models.CharField(max_length=256, db_index=True)  # 用户昵称

    focus_cities = models.TextField(default=[])  # 关注的城市
    focus_stars = models.TextField(default=[])  # 关注的星座
    focus_stock = models.TextField(default=[])  # 关注的股票

    # menu = models.ManyToManyField(App)  # 用户和App的多对多关系

    class Meta:
        indexes = [
            # models.Index(fields=['nickname']),
            models.Index(fields=['open_id', 'nickname'])
        ]

    def __str__(self):
        return self.nickname
