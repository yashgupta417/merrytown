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
    url(r'shot_list/$',views.ShotListAPIView.as_view(),name="shot_list_api"),
    url(r'shot_detail/$',views.ShotDetailAPIView.as_view(),name="shot_detail_api"),
    url(r'comment_list/$',views.CommentListAPIView.as_view(),name="comment_list_api"),
    url(r'comment_detail/$',views.CommentDetailAPIView.as_view(),name="comment_detail_api"),        



]
# from rest_framework.authtoken import views as rest_framework_views
urlpatterns += [
    url(r'^login/$', views.CustomAuthToken.as_view(),name="login"),
    url(r'^logout/(?P<id>\d+)/$',views.LogoutView.as_view(),name="logout")
]
