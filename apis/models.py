# from django.db import models
#
#
# class App(models.Model):
#     """
#     入口功能清单描述
#     """
#     appid = models.CharField(primary_key=True, max_length=32)  # id
#     category = models.CharField(max_length=128)  # 分类
#     name = models.CharField(max_length=32)  # 应用名
#     publish_date = models.DateTimeField()  # 发布日期
#     url = models.CharField(max_length=128)  # url地址
#     desc = models.TextField()  # 应用描述
#
#     def to_dict(self):
#         return {
#             'appid': self.appid,
#             'category': self.category,
#             'name': self.name,
#             'publish_date': self.publish_date,
#             'url': self.url,
#             'desc': self.desc
#         }
#
#     def __str__(self):
#         return str(self.to_dict())
#
#     # def __repr__(self):
#     #     return str(self.to_dict())
