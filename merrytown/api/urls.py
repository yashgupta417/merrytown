from django.conf.urls import url
from . import views
app_name='api'
urlpatterns=[
    url(r'signup/$',views.SignupAPIView.as_view(),name="signup_api"),
    url(r'^user_detail/(?P<username>\w+)/$',views.UserDetailAPIView.as_view(),name="user_detail_api"),
    url(r'message_list/$',views.MessageListAPIView.as_view(),name="message_list_api"),
    url(r'message_detail/$',views.MessageDetailAPIView.as_view(),name="message_detail_api"),
    # url(r'chat_room_list/$',views.ChatRoomListAPIView.as_view(),name="chat_room_list_api"),
    # url(r'chat_room_detail/$',views.ChatRoomDetailAPIView.as_view(),name="chat_room_detail_api"),
    url(r'gcm_list/$',views.GCMDeviceListAPIView.as_view(),name="gcm_list_api"),
    url(r'gcm_detail/$',views.GCMDeviceDetailAPIView.as_view(),name="gcm_detail_api"),

]
# from rest_framework.authtoken import views as rest_framework_views
urlpatterns += [
    url(r'^login/$', views.CustomAuthToken.as_view(),name="login"),
    url(r'^logout/(?P<id>\d+)/$',views.LogoutView.as_view(),name="logout")
]
