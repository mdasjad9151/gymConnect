import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import PrivateMessage
import datetime

User =  get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.friend_id = self.scope['url_route']['kwargs']['user_id']
        self.user = self.scope.get("user")

        if self.user.is_authenticated:
            self.room_name = f"chat_{min(str(self.user.id), str(self.friend_id))}_{max(str(self.user.id), str(self.friend_id))}"
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            await self.send_undelivered_messages()
        else:
            await self.close()

    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        #  Save message in database asynchronously
        await self.save_message(self.user.id, self.friend_id, message)


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.id,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        # Don't send the message back to the sender
        if event['sender'] != self.user.id:
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
                'timestamp': event['timestamp'],
            }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        PrivateMessage.objects.create(sender=sender, receiver=receiver, message=message)

    @database_sync_to_async
    def get_undelivered_messages(self):
        messages = PrivateMessage.objects.filter(receiver__id=self.user.id, is_delivered=False)
        return [
            {
                "message": msg.message,
                "sender": msg.sender.id,
                "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for msg in messages
        ]

    async def send_undelivered_messages(self):
        undelivered_messages = await self.get_undelivered_messages()
        for msg in undelivered_messages:
            await self.send(text_data=json.dumps(msg))

        #  Mark them as delivered
        await self.mark_messages_as_delivered()

    @database_sync_to_async
    def mark_messages_as_delivered(self):
        PrivateMessage.objects.filter(receiver__id=self.user.id, is_delivered=False).update(is_delivered=True)



# notifications

# consumers.py


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_notify_{self.scope['user'].id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def reload_connections(self, event):
        await self.send(text_data=json.dumps({
            "action": "reload"
        }))
