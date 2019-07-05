from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
# Create your models here.
class User(AbstractUser):

    image=models.ImageField(upload_to="images/%Y/%m/%D/",blank=True,null=True)
    is_logged_in=models.BooleanField(default=False,blank=True,null=True)
    is_active=models.BooleanField(default=True)


# class ChatRoom(models.Model):
#     person1=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="chat_rooms_as_person_1",on_delete=models.CASCADE)
#     person2=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="chat_rooms_as_person_2",on_delete=models.CASCADE)

class Message(models.Model):
    text=models.TextField()
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages_as_sender',on_delete=models.CASCADE)
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages_as_recipient',on_delete=models.CASCADE)
    date_of_messaging=models.DateTimeField(default=timezone.now)
    seen=models.BooleanField(default=False)

#hey
#hi again
#hi 2
