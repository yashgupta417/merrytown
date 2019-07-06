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

class CommentSerializer(serializers.ModelSerializer):
    commented_by=UserSerializer(many=True)
    shot=ShotSerializer(many=True)
    class Meta():
        model=Comment
        fields=['text','commented_by','date','shot']
        depth=1

    def create(self, validated_data):
        commented_by= validated_data.pop('commented_by')
        shot=validated_data.pop('shot')
        comment = Comment.objects.create(**validated_data)
        comment.commented_by=commented_by
        comment.shot=shot
        comment.save()
        return comment



class ShotSerializer(serializers.ModelSerializer):
    comments_on_this_shot=CommentSerializer(many=True,read_only=True)
    by=UserSerializer(many=True)
    to=UserSerializer(many=True)
    class Meta():
        model=Shot
        fields=['title','text','image','by','to','date','comments_on_this_shot']
        depth=1

    def create(self, validated_data):
        by= validated_data.pop('by')
        to=validated_data.pop('to')
        shot = Shot.objects.create(**validated_data)
        shot.by=by
        shot.to=to
        shot.save()

        return shot
