from .models import Message,Group,GroupMessage
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
            instance.status="On Server"
            instance.save()
            sender=instance.sender
            recipient=instance.recipient
            r_id=recipient.id
            s_id=sender.id
            s_username=sender.username
            s_first_name=sender.first_name
            s_last_name=sender.last_name
            s_email=sender.email
            if sender.image:
                s_image='http://yashgupta4172.pythonanywhere.com'+sender.image.url
            else:
                 s_image=None
            if instance.image:
                m_image='http://yashgupta4172.pythonanywhere.com'+instance.image.url
            else:
                m_image=None
            device.send_message(None,extra={"recipient_id":r_id,
                                        "sender_id":s_id,"s_username":s_username,"s_first_name":s_first_name,
                                        "s_last_name":s_last_name,"s_email":s_email,"s_image":s_image,
                                        "id":instance.id,
                                        "text":instance.text,"date":instance.date,"time":instance.time,"amorpm":instance.amorpm,"image":m_image})

import uuid
from datetime import datetime
@receiver(post_save,sender=Group)
def group_created(sender,instance=None,created=False,**kwargs):
    if created:
        event="Group created by @"+instance.president.username
        date_time=datetime.now()
        id=uuid.uuid1()
        d=date_time.strftime("%Y-%m-%d")
        t=date_time.strftime("%I:%M:%S")
        amorpm=date_time.strftime("%p")
        instance.datetime_of_creation=d+" "+t+" "+amorpm
        instance.save()
        message=GroupMessage(event=event,id=id,date=d,time=t,amorpm=amorpm,group=instance,sender=instance.president)
        message.save()


@receiver(post_save,sender=GroupMessage)
def send_group_message(sender,instance=None,created=False,**kwargs):
    if created:
        for member in instance.group.members.all():
            if(member.is_logged_in):
                device=GCMDevice.objects.get(user=member)
                device.cloud_message_type='FCM'
                if instance.group.group_image:
                    g_image='http://yashgupta4172.pythonanywhere.com'+instance.group.group_image.url
                else:
                    g_image=None
                if instance.sender.image:
                    s_image='http://yashgupta4172.pythonanywhere.com'+instance.sender.image.url
                else:
                    s_image=None
                if instance.image:
                    m_image='http://yashgupta4172.pythonanywhere.com'+instance.image.url
                else:
                    m_image=None
                device.send_message(None,extra={'group_id':instance.group.id,'group_name':instance.group.group_name,
                                                    'group_image':g_image,
                                                    'sender_id':instance.sender.username,'sender_name':instance.sender.first_name,
                                                    'sender_image':s_image,
                                                    'group_message_id':instance.id,
                                                    'text':instance.text,'event':instance.event,'date':instance.date,'time':instance.time,
                                                    'amorpm':instance.amorpm,'image':instance.image})
