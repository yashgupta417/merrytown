from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,ChatRoom,Message
# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(Message)

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
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image', 'is_logged_in',)}),
    )

admin.site.register(User, MyUserAdmin)
