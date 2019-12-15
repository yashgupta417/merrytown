from django.conf.urls import url
from . import views
app_name='api'
urlpatterns=[
    url(r'signup/$',views.SignupAPIView.as_view(),name="signup_api"),
    url(r'^user_detail/(?P<username>\w+)/$',views.UserDetailAPIView.as_view(),name="user_detail_api"),
    url(r'message_list/$',views.MessageListAPIView.as_view(),name="message_list_api"),
    url(r'message_detail/$',views.MessageDetailAPIView.as_view(),name="message_detail_api"),
    url(r'create_fcm_token/$',views.CreateFCMTokenView.as_view(),name="create_fcm_token_api"),
    url(r'update_fcm_token/$',views.UpdateFCMTokenView.as_view(),name="update_fcm_token_api"),
    url(r'update_message_status/$',views.UpdateMessageStatusAPIView.as_view(),name="update_message_status_api"),
    url(r'get_last_seen/$',views.getLastSeenAPIView.as_view(),name="get_last_seen_api"),
    url(r'user_list/$',views.UserQueryAPIView.as_view(),name="user_query_api"),
    url(r'group_list/$',views.GroupCreateAPIView.as_view(),name="group_list_api"),
    url(r'send_group_message/$',views.GroupMessageListAPIView.as_view(),name="group_message_list_api"),
    url(r'add_member/$',views.addMemberAPIView.as_view(),name="add_member_api_view"),
    url(r'send_group_message/$',views.GroupMessageListAPIView.as_view(),name='send_group_message_api'),
    url(r'group_detail/(?P<group_id>\w+)/$',views.GroupDetailAPIView.as_view(),name='group_detail_api'),
    url(r'memory_create/$',views.MemoryCreateAPIView.as_view(),name='memory_create_api'),
    url(r'memory_list/$',views.MemoryListAPIView.as_view(),name='memory_list_api'),
    url(r'memory_detail/$',views.MemoryDetailAPIView.as_view(),name='memory_detail_api'),
    url(r'group_query/$',views.GroupQueryAPIView.as_view(),name='group_query_api'),
    url(r'follow_group/$',views.FollowGroupAPIView.as_view(),name='follow_group_api'),

]
# from rest_framework.authtoken import views as rest_framework_views
urlpatterns += [
    url(r'^login/$', views.CustomAuthToken.as_view(),name="login"),
    url(r'^logout/(?P<id>\d+)/$',views.LogoutView.as_view(),name="logout")
]
