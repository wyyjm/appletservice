from django.contrib import admin
from .models import User

# admin.site.register(User)


@admin.register(User)  # 表示把User模块注册到admin里面
class AuthorizationUserAdmin(admin.ModelAdmin):
    """
    自定义admin
    """
    exclude = ['open_id']  # 不显示open_id
    fields = ['nickname', 'focus_cities', 'focus_stars']  # 指定显示字段
    pass