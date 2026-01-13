from rest_framework import serializers
from .models import User, UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    """用户地址序列化器"""
    
    class Meta:
        model = UserAddress
        fields = ['id', 'receiver_name', 'receiver_phone', 'province', 'city', 
                  'district', 'address', 'postal_code', 'is_default', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    addresses = UserAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar_url', 'status', 
                  'last_login_at', 'addresses', 'created_at', 'updated_at']
        read_only_fields = ['last_login_at', 'created_at', 'updated_at']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname']
    
    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value
    
    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
