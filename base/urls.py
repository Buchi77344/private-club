from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name="index"),
    path('forget',forget, name="forget"),
    path('signup',signup, name="signup"),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
]
