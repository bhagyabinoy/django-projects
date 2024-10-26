import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from chatapp.models import Room,Message,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        pass
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_name = text_data_json["room_name"]
        
        await self.save_message(message, username, room_name)     

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
    
    @sync_to_async
    def save_message(self, message, username, room_name):
        print(username,room_name,"----------------------")
        user=User.objects.get(username=username)
        room=Room.objects.get(name=room_name)
        
        Message.objects.create(user=user,room=room,content=message)
















# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         self.send(text_data=json.dumps({
#             'type':"connection established",
#             'message':"You are now connected",
#         }))
        
#     def disconnect(self, close_code):

#         self.send(text_data=json.dumps({
#             'type': 'connection closed',
#             'message': 'Connection closed. Goodbye!',
#         }))
