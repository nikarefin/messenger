import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, UserProfile, ChatRoom
from channels.db import database_sync_to_async


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        await self.accept()

        await self.display_chat_history(self.room_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user_name = text_data_json['user_name']

        await self.save_message(user_id, self.room_id, message)

        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'user_name': user_name
            }
        )

    @database_sync_to_async
    def save_message(self, user_id, room_id, content):
        user = UserProfile.objects.get(id=user_id)
        room, created = ChatRoom.objects.get_or_create(id=room_id)
        Message.objects.create(author=user, chat=room, content=content)

    @database_sync_to_async
    def get_author_name(self, message):
        return message.author.name

    async def display_chat_history(self, room_id):
        room = await sync_to_async(ChatRoom.objects.get)(id=room_id)
        messages = await sync_to_async(Message.objects.filter)(chat=room)
        messages = await sync_to_async(list)(messages.order_by("timestamp"))

        for message in messages:
            author_name = await self.get_author_name(message)
            await self.send(text_data=json.dumps({
                'user_name': author_name,
                'message': message.content,
                'timestamp': str(message.timestamp)
            }))

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_name = event['user_name']

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'user_name': user_name
        }))
