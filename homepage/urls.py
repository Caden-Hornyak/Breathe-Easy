from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('prompt_reciever/', views.prompt_reciever, name="prompt_reciever"),
    path('send_friend_request/', views.send_friend_request, name="send_friend_request"),
    path('accept_friend_request/', views.accept_friend_request, name="accept_friend_request"),
    path('message_action/', views.message_action, name="message_action"),
    path('get_chats/', views.get_chats, name='get_chats'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('friends/', views.friends, name='friends'),
    path('get_friend_request/', views.get_friend_request, name='get_friend_request'),
]
