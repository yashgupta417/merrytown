from rest_framework import generics
from rest_framework.views import APIView
from .serializers import MessageSerializer,UserSerializer,GCMDeviceSerializer
from app_one.models import Message
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
class SignupAPIView(generics.CreateAPIView):
    serializer_class=UserSerializer
    # authentication_classes=[]
    # permission_classes=[]
    def get_queryset(self):
        return get_user_model().objects.all()

class UserQueryAPIView(generics.ListAPIView):
    serializer_class=UserSerializer
    def get_queryset(self):
        query=self.request.query_params.get('query',None)
        if query!=None:
            return get_user_model().objects.filter(Q(username__istartswith=query)|Q(first_name__istartswith=query)).exclude(username='admin')
        return get_user_model().objects.all()

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        username=self.kwargs.get('username')
        user=get_user_model().objects.get(username=username)
        return  user

class MessageListAPIView(generics.ListCreateAPIView):
    serializer_class=MessageSerializer

    def get_queryset(self):
        return Message.objects.all()

class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=MessageSerializer

    def get_queryset(self):
        return Message.objects.all()

    def get_object(self):
        id=self.kwargs.get('id')
        return Message.objects.get(id=id)

from .serializers import GroupReadSerializer,GroupWriteSerializer,GroupMessageSerializer
from app_one.models import Group
class GroupListAPIView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return GroupReadSerializer
        else:
            return GroupWriteSerializer
    def get_queryset(self):
        return Group.objects.all()

class GroupMessageListAPIView(generics.ListCreateAPIView):
    serializer_class=GroupMessageSerializer

    def get_queryset(self):
        return GroupMessage.objects.all()

from django.db.models import Q

class ShotListAPIView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST':
            return ShotWriteSerializer
        else:
            return ShotReadSerializer
    def get_queryset(self):
        id_me=self.request.query_params['id_me']
        id_friend=self.request.query_params['id_friend']
        # return Shot.objects.filter(Q(by__id=id_me),Q(to__id=id_friend)|Q(by__id=id_friend),Q(to__id=id_me))
        return Shot.objects.filter(Q(by__id=id_me,to__id=id_friend)|Q(by__id=id_friend,to__id=id_me))




class ShotDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        method = self.request.method
        if method == 'PATCH' or method=='PUT':
            return ShotWriteSerializer
        else:
            return ShotReadSerializer

    def get_queryset(self):
        return Shot.objects.all()

    def get_object(self):
        id=self.kwargs.get('id')
        return Shot.objects.get(id=id)


class CommentListAPIView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        method = self.request.method
        if method == 'POST':
            return CommentWriteSerializer
        else:
            return CommentReadSerializer

    def get_queryset(self):
        return Comment.objects.all()

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        method = self.request.method
        if method == 'PATCH' or method=='PUT':
            return CommentWriteSerializer
        else:
            return CommentReadSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def get_object(self):
        id=self.kwargs.get('id')
        return Comment.objects.get(id=id)

from push_notifications.models import GCMDevice

class CreateFCMTokenView(generics.ListCreateAPIView):
    serializer_class=GCMDeviceSerializer
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    #send registration_id,user and cloud_message_type='FCM'
    def get_queryset(self):
        return GCMDevice.objects.all()


class UpdateFCMTokenView(APIView):
    def patch(self,request,*args,**kwargs):
        id=self.request.query_params['user']
        fcm_token=self.request.query_params['registration_id']
        device=GCMDevice.objects.get(user=id)
        device.registration_id=fcm_token
        device.save()
        return Response({'user':device.user.id,'registration_id':device.registration_id})



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if(user.is_logged_in):
            return Response({
            'token':None
            })

        #else everything is ok
        user.is_logged_in=True
        user.save()
        token, created= Token.objects.get_or_create(user=user)
        if user.image:
            image='http://yashgupta4172.pythonanywhere.com'+user.image.url
        else:
            image=None
        return Response({
            'token': token.key or created.key,
            'id': user.id,
            'username': user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            # #is_logged_in is for checking purpose only so that only user can login from one device

            'image':  image,
        })

class LogoutView(APIView):
    def post(self,request,*args,**kwargs):
        id=self.kwargs['id']
        user=get_user_model().objects.get(id=id)
        user.is_logged_in=False
        user.save()
        device=GCMDevice.objects.get(user=user)
        device.delete()
        return Response({
        'token':None
        })

class UpdateMessageStatusAPIView(APIView):

    def post(self,request,*args,**kwargs):
        message_id=self.request.query_params['id']
        status=self.request.query_params['status']
        message=Message.objects.get(id=message_id)
        if message.status=='Seen':
            return Response({})
        message.status=status
        message.save()
        sender_device=GCMDevice.objects.get(user=message.sender)
        sender_device.cloud_message_type='FCM'
        sender_device.send_message(None,extra={'type':2,'id':message_id,'status':status})
        return Response({})

class getLastSeenAPIView(APIView):
    def get(self,request,*args,**kwargs):
        username=self.request.query_params['username']
        user=get_user_model().objects.get(username=username)
        return Response({'last_seen_time':user.last_seen_time,'last_seen_date':user.last_seen_date})

from app_one.models import User
class addMemberAPIView(APIView):
    def post(self,request,*args,**kwargs):
        group_id=self.request.query_params['group_id']
        user_id=self.request.query_params['user_id']
        group=Group.objects.get(id=group_id)
        group.members.add(User.objects.get(id=user_id))
        group.save()
        return Response({'message':'success'})
