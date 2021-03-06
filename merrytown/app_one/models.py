from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
class User(AbstractUser):

    image=models.ImageField(upload_to="images/%Y/%m/%D/",blank=True,null=True)
    is_logged_in=models.BooleanField(default=False,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    last_seen_date=models.TextField(default="1 feb 2001")
    last_seen_time=models.TextField(default="00:00")
    # is_typing=models.BooleanField(default=False)


class Message(models.Model):
    id=models.TextField(primary_key=True)
    text=models.TextField(blank=True,null=True)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages_as_sender',on_delete=models.CASCADE)
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages_as_recipient',on_delete=models.CASCADE)
    image=models.ImageField(upload_to="messageImage/",blank=True,null=True)
    # date_of_messaging=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=255,default="sending")
    date=models.TextField(default="default date")
    time=models.TextField(default="default time")
    amorpm=models.TextField(default="$")
    def __str__(self):
        return str(self.id)

from django.utils import timezone
class Group(models.Model):
    group_name=models.TextField()
    group_image=models.ImageField(upload_to="group_dp/",blank=True,null=True)
    members=models.ManyToManyField(get_user_model(),related_name='user_groups',blank=True)
    president=models.ForeignKey(get_user_model(),related_name='president_of_groups',on_delete=models.CASCADE,null=True,blank=True)
    datetime_of_creation=models.DateTimeField(default=timezone.now)
    followers=models.ManyToManyField(get_user_model(),related_name='groups_following',blank=True)
    def __str__(self):
        return str(self.id)+" "+self.group_name

class GroupMessage(models.Model):
    id=models.TextField(primary_key=True)
    event=models.TextField(blank=True,null=True)
    text=models.TextField(blank=True,null=True)
    sender=models.ForeignKey(get_user_model(),related_name='group_messages',on_delete=models.CASCADE,null=True,blank=True)
    group=models.ForeignKey('Group',related_name='messages_of_this_group',on_delete=models.CASCADE)
    image=models.ImageField(upload_to="messageImage/",blank=True,null=True)
    #status=models.CharField(max_length=255,default="sending")
    date=models.TextField(default="default date")
    time=models.TextField(default="default time")
    amorpm=models.TextField(default="$")
    def __str__(self):
        return str(self.id)

#https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

class Memory(models.Model):
    group=models.ForeignKey('Group',related_name='memories',on_delete=models.CASCADE)
    member_posted=models.ForeignKey(get_user_model(),related_name='memories_posted_by_me',on_delete=models.CASCADE)
    image=models.FileField(upload_to='memories/')
    text=models.TextField(blank=True,null=True)
    date=models.DateTimeField(default=timezone.now)
