from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name="index"),
    path('forget',forget, name="forget"),
    path('signup',signup, name="signup"),
    path('member/',member, name="member"),
    path("send-referrals", send_referrals, name="send_referrals"),
    path("check-declined-referrals/", check_declined_referrals, name="check_declined_referrals"),
    path("check-referral-approval/", check_referral_approval, name="check-referral-approval"),
    path('payment/',payment, name="payment"),
    path('status/',status, name="status"),
    path("check-referral-status/", check_referral_status, name="check_referral_status"),
    path('login',login, name="login"),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path("get-token/", get_token, name="get_token"),
    path("send-message/", send_message, name="send_message"),
    path("add-referral/", add_referral, name="add_referral"),
    path("chat/", chat_page, name="chat"),
]




