from rest_framework import generics
from rest_framework.views import APIView
from .serializers import MessageSerializer,ChatRoomSerializer,UserSerializer,GCMDeviceSerializer
from app_one.models import Message,ChatRoom
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
class SignupAPIView(generics.ListCreateAPIView):
    serializer_class=UserSerializer
    # authentication_classes=[]
    # permission_classes=[]
    def get_queryset(self):
        return get_user_model().objects.all()

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        id=self.kwargs.get('id')
        return get_user_model().objects.get(id=id)

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

class ChatRoomListAPIView(generics.ListCreateAPIView):
    serializer_class=ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.all()

class ChatRoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ChatRoomSerializer
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return ChatRoom.objects.all()

    def get_object(self):
        id=self.kwargs.get('id')
        return ChatRoom.objects.get(id=id)

from push_notifications.models import GCMDevice

class GCMDeviceListAPIView(generics.ListCreateAPIView):
    serializer_class=GCMDeviceSerializer
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return GCMDevice.objects.all()

class GCMDeviceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=GCMDeviceSerializer
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return GCMDevice.objects.all()

    def get_object(self):
        user=self.kwargs.get('user')
        return GCMDevice.objects.get(user=user)

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
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'is_logged_in':user.is_logged_in,
            'image':user.image
        })

class LogoutView(APIView):
    def post(self,request,*args,**kwargs):
        id=self.kwargs['id']
        user=get_user_model().objects.get(id=id)
        user.is_logged_in=False
        user.save()
        return Response({
        'is_logged_in':False
        })
