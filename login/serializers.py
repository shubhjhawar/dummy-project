from rest_framework import serializers
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username", "email", "first_name", "last_name", "date_joined")

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': "email already exists"})
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': "username already exists"})
        return super().validate(attrs)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = "__all__"

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeyModel
        fields = "__all__"

class RemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarkModel
        fields = ["remark"]


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonModel
        fields = ["reason"]

# class UserStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserStatusModel
#         fields = "__all__"