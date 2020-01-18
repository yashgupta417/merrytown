from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Message,Group,GroupMessage,Memory
# Register your models here.

# admin.site.register(ChatRoom)
#admin.site.register(Message)
admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(Memory)


from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    ordering = ('-date_joined', )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image', 'is_logged_in','last_seen_date','last_seen_time')}),
    )

class MessageAdmin(ModelAdmin):
    list_display=['id','sender','recipient','text','date','time','amorpm']
    list_filter=['sender','recipient']
    search_fields=['text']

admin.site.register(User, MyUserAdmin)
admin.site.register(Message,MessageAdmin)
