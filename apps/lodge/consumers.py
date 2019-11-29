import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer


class LodgeConsumer(WebsocketConsumer):
    groups = ['Editor']

    def connect(self):
        user = self.scope['user']
        for group in user.groups.all():
            async_to_sync(self.channel_layer.group_add)(
                group.name,
                self.channel_name
            )
        super(LodgeConsumer, self).connect()

    def disconnect(self, close_code):
        # Leave room group
        user = self.scope['user']
        for group in user.groups.all():
            self.channel_layer.group_discard(group.name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        group_name = text_data_json['group_name']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'lodge': 'editor',
            'user_id': self.scope['user'].id
        }))


class Lodge2Consumer(AsyncJsonWebsocketConsumer):
    groups = ['Editor']

    async def connect(self):
        user = self.scope['user']
        for group in user.groups.all():
            await self.channel_layer.group_add(
                group.name,
                self.channel_name
            )

            await self.accept()

    async def send_data(self, event):
        await self.send_json(event)
        print(f'Got message {event} at {self.channel_name}')

    async def disconnect(self, close_code):
        for group in list(self.groups):
            await self.channel_layer.group_discard(str(group), self.channel_name)
        print(f'Removed {self.channel_name} channel')

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
            'lodge': 'editor',
            'user_id': self.scope['user'].id
        }))