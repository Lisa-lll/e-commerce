from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    """用户表（可选，支持未登录用户下单）"""
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password_hash = models.CharField(max_length=255, verbose_name='密码哈希')
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称')
    avatar_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像URL')
    status = models.IntegerField(default=1, verbose_name='状态', help_text='1-正常, 0-禁用')
    last_login_at = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['status']),
        ]

    def set_password(self, raw_password):
        """设置密码"""
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    """用户收货地址表（仅登录用户）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    receiver_name = models.CharField(max_length=50, verbose_name='收货人姓名')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货人电话')
    province = models.CharField(max_length=50, verbose_name='省份')
    city = models.CharField(max_length=50, verbose_name='城市')
    district = models.CharField(max_length=50, verbose_name='区县')
    address = models.CharField(max_length=255, verbose_name='详细地址')
    postal_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='邮编')
    is_default = models.IntegerField(default=0, verbose_name='是否默认地址', help_text='0-否, 1-是')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_addresses'
        verbose_name = '用户地址'
        verbose_name_plural = '用户地址'
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.receiver_name} - {self.receiver_phone}"
