from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_id']

        self.group_name = f'Chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        user_send = text_data_json['user_send']
        users_receive = text_data_json['users_receive']
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'message',
                'user_send': user_send,
                'users_receive': users_receive
            }
        )

    async def message(self, event):
        user_send = event.get('user_send')
        users_receive = event.get('users_receive')
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                'event': "Update",
                'user_send': user_send,
                'users_receive': users_receive,

            })
        )
