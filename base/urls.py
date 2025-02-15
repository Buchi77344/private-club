from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name="index"),
    path('forget',forget, name="forget"),
    path('signup',signup, name="signup"),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path("get-token/", get_token, name="get_token"),
    path("send-message/", send_message, name="send_message"),
    path("chat/", chat_page, name="chat"),
]




