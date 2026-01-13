from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Admin(models.Model):
    """管理员表（简化权限，单角色）"""
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password_hash = models.CharField(max_length=255, verbose_name='密码哈希')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='真实姓名')
    status = models.IntegerField(default=1, verbose_name='状态', help_text='1-正常, 0-禁用')
    last_login_at = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'admins'
        verbose_name = '管理员'
        verbose_name_plural = '管理员'
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
