import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle the received message, e.g., save it to the database

        # Notify the user about the new message
        await self.send(text_data=json.dumps({'message': 'New message received!'}))