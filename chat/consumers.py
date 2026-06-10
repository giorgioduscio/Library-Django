import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import Message, Room
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Unisciti al gruppo della stanza
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Lascia il gruppo della stanza
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('text')
        
        if not message_text:
            return

        user = self.scope['user']
        if not user.is_authenticated:
            return

        # Salva il messaggio nel database
        message_obj = await self.save_message(user, self.room_name, message_text)

        # Renderizza il fragment HTML
        html_message = render_to_string('chat/message_snippet.html', {'msg': message_obj})

        # Invia il messaggio al gruppo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'html': html_message
            }
        )

    async def chat_message(self, event):
        html = event['html']

        # Invia l'HTML direttamente al WebSocket
        await self.send(text_data=html)

    @database_sync_to_async
    def save_message(self, user, room_name, text):
        room = Room.objects.get(name=room_name)
        return Message.objects.create(user=user, room=room, text=text)
