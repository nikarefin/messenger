from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django.shortcuts import render
from chats.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class UserProfilesViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all().order_by('-updated_at')
    serializer_class = ChatRoomSerializer


class CurrentUserChatsViewSet(ModelViewSet):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(members__in=[user.profile], is_group=False)


@login_required
def profile_edit(request):
    return render(request, 'chats/profile-edit.html')


@login_required
def chats(request):
    return render(request, 'chats/chats.html')


@login_required
def chatroom_create(request):
    return render(request, 'chats/chatroom-create.html')


@login_required
def chat_create(request):
    return render(request, 'chats/chat-create.html')


@login_required
def chatroom_members(request, room_id):
    room = ChatRoom.objects.get(id=room_id)
    return render(request, 'chats/chatroom-members.html', {
        'room': room
    })


@login_required
def chatroom_edit(request, room_id):
    room = ChatRoom.objects.get(id=room_id)
    return render(request, 'chats/chatroom-edit.html', {
        'room': room
    })


@login_required
def room(request, room_id):
    room = ChatRoom.objects.get(id=room_id)
    if not room.is_group:
        for member in room.members.all():
            if str(member.name) != str(request.user.profile.name):
                room.name = member.name
                break
    return render(request, 'chats/room.html', {
        'room_id': room.id,
        'room_name': room.name,
        'room_is_group': room.is_group
    })


@receiver(pre_save, sender=UserProfile)
def save_old_name(sender, instance, **kwargs):
    try:
        old = UserProfile.objects.get(id=instance.id)
        instance.old_name = old.name
    except UserProfile.DoesNotExist:
        instance.old_name = None


@receiver(post_save, sender=UserProfile)
def update_chatroom_name(sender, instance, **kwargs):
    if hasattr(instance, 'old_name') and instance.old_name and instance.old_name != instance.name:
        ChatRoom.objects.filter(name=instance.old_name, members=instance).update(name=instance.name)
