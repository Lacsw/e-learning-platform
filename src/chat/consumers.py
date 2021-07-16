import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # принимает соединение
        self.accept()

    def disconnect(self, close_code):
        pass

    # получает сообщение от WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # отправляет сообщение к WebSocket
        self.send(text_data=json.dumps({'message': message}))
