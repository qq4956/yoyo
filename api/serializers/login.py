from rest_framework import serializers
from ..models import *

class LoginSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30)
    avatar_url = serializers.URLField()
    gender = serializers.CharField(max_length=10)
    province =  serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return UserInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance
