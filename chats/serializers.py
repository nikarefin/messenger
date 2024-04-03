from rest_framework import serializers
from .models import UserProfile, ChatRoom


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'user_pic']


class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'members', 'is_group', 'chat_pic']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        chat_room = ChatRoom.objects.create(**validated_data)

        for member_data in members_data:
            member, created = UserProfile.objects.get_or_create(**member_data)
            chat_room.members.add(member)
        return chat_room

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members')
        instance.name = validated_data.get('name', instance.name)
        instance.is_group = validated_data.get('is_group', instance.is_group)
        instance.chat_pic = validated_data.get('chat_pic', instance.chat_pic)

        instance.members.clear()

        for member_data in members_data:
            member, created = UserProfile.objects.get_or_create(
                name=member_data.get('name'),
                defaults={'id': member_data.get('id', None)})

            instance.members.add(member)

        instance.save()
        return instance


