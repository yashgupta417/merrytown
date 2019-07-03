from .models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from push_notifications.models import APNSDevice, GCMDevice
from django.conf import settings
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_superuser==False:
            instance.set_password(instance.password)
            instance.save()
        instance.is_active=True
        instance.save()
        Token.objects.create(user=instance)


@receiver(post_save,sender=Message)
def send_message(sender,instance=None,created=False,**kwargs):
    if created:
        if(instance.recipient.is_logged_in):
            device=GCMDevice.objects.get(user=instance.recipient)
            device.cloud_message_type='FCM'
            sender=instance.sender
            recipient=instance.recipient
            r_id=recipient.id
            s_id=sender.id
            s_username=sender.username
            s_first_name=sender.first_name
            s_last_name=sender.last_name
            s_email=sender.email
            if sender.image:
                s_image='yashgupta4172.pythonanywhere.com'+sender.image.url
            else:
                 s_image=None
            device.send_message(instance.text,extra={"title":s_first_name,"recipient":r_id,
                                                        "sender":s_id,"s_username":s_username,"s_first_name":s_first_name,
                                                        "s_last_name":s_last_name,"s_email":s_email,"s_image":s_image})
        # device=GCMDevice.objects.get(user=instance.recipient)#user is ForeignKey to auth.user,so we can not use it here
        # if device.active:
        #     sender=instance.sender.username
        #     recipient=instance.recipient.username
        #     chat_room_id=instance.chat_room.id
        #     device.send_message(instance.text,extra={"title":sender,"from":sender,"to":recipient,"chat_room_id":chat_room_id})
