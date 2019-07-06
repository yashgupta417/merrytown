from rest_framework import generics
from rest_framework.views import APIView
from .serializers import MessageSerializer,UserSerializer,GCMDeviceSerializer,ShotWriteSerializer,ShotReadSerializer,CommentWriteSerializer,CommentReadSerializer
from app_one.models import Message,Shot,Comment
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
        username=self.kwargs.get('username')
        return get_user_model().objects.get(username=username)

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

    def create(self, request, *args, **kwargs):
        serializer = ShotWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"Success": "true"}, status=status.HTTP_201_CREATED, headers=headers)


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
