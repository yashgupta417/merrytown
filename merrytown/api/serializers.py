from app_one.models import Message,Group,GroupMessage,Memory
from rest_framework import serializers
from django.conf import settings
from push_notifications.models import GCMDevice
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model=get_user_model()
        fields='__all__'
        read_only_fields=['id',]



class MessageSerializer(serializers.ModelSerializer):
    class Meta():
        model=Message
        fields='__all__'

class GroupWriteSerializer(serializers.ModelSerializer):
    class Meta():
        model=Group
        fields='__all__'

class GroupReadSerializer(serializers.ModelSerializer):
    class Meta():
        model=Group
        fields='__all__'
        depth=1

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta():
        model=GroupMessage
        fields='__all__'

class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta():
        model=GCMDevice
        fields='__all__'

class MemoryReadSerializer(serializers.ModelSerializer):
    class Meta():
        model=Memory
        fields='__all__'
        depth=1

class MemoryWriteSerializer(serializers.ModelSerializer):
    class Meta():
        model=Memory
        fields='__all__'

class UserDetailSerializer(serializers.ModelSerializer):
    groups_following=GroupWriteSerializer(many=True,read_only=True)
    class Meta():
        model=get_user_model()
        fields='__all__'
        read_only_fields=['id',]
