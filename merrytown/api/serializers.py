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
    class Meta():
        model=Comment
        fields='__all__'
        depth=1

    def create(self, validated_data):
        commented_by_id = validated_data.pop('commented_by')
        comment = Comment.objects.create(**validated_data)
        user=get_user_model().objects.get(id=commented_by_id)
        comment.commented_by=user
        comment.save()
        return comment



class ShotSerializer(serializers.ModelSerializer):
    comments_on_this_shot=CommentSerializer(many=True,read_only=True)
    class Meta():
        model=Shot
        fields=['title','text','image','by','to','date','comments_on_this_shot']
        depth=1

    def create(self, validated_data):
        by_id = validated_data.pop('by')
        to_id=validated_data.pop('to')
        shot = Shot.objects.create(**validated_data)
        by_user=get_user_model().objects.get(id=by_id)
        to_user=get_user_model().objects.get(id=to_id)
        shot.by=by_user
        shot.to=to_user
        shot.save()

        return shot
