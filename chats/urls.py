from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

route = DefaultRouter()

route.register(r'api/profiles', UserProfilesViewSet)
route.register(r'api/chat-rooms', ChatRoomViewSet)
route.register(r'api/current_user_chats', CurrentUserChatsViewSet, basename='current_user_chats')

urlpatterns = [
    path('', chats, name='chats'),
    path('chatroom-create/', chatroom_create, name='chatroom_create'),
    path('chats-create/', chat_create, name='chat_create'),
    path('profile-edit/', profile_edit, name='profile_edit'),
    path('chatroom-edit/<str:room_id>/', chatroom_edit, name='chatroom_edit'),
    path('chatroom-members/<str:room_id>/', chatroom_members, name='chatroom_members'),
    path('<str:room_id>/', room, name='room'),
] + route.urls
