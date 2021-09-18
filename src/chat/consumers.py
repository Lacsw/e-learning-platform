import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # вход в чат курса
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # принимает соединение
        await self.accept()

    async def disconnect(self, close_code):
        #  выход из чата
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # получает сообщение от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # отправляет сообщение к WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    # получение сообщения от чата курса
    async def chat_message(self, event):
        # отправка сообщения к WebSocket
        await self.send(text_data=json.dumps(event))
