from app_one.models import Message,Shot,Comment
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

# class ChatRoomSerializer(serializers.ModelSerializer):
#     class Meta():
#         model=ChatRoom
#         fields='__all__'

class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta():
        model=GCMDevice
        fields='__all__'

class ShotSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True,read_only=True)
    class Meta():
        model=Shot
        fields='__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta():
        model=Comment
        fields='__all__'
