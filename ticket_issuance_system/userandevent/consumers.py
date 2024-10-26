# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = 'chat_group'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
        
#     async def disconnect(self, close_code):
#         pass
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
        
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print(text_data_json,"received msg from server-------------------------------")
#         message = text_data_json["message"]
#         userid = text_data_json["user"]
#         sender = text_data_json["sender"]
        
#         #await self.save_message(message, username)     

#         await self.channel_layer.group_send(
#             self.room_group_name, {
#                 "type": "sendMessage",
#                 "message": message,
#                 "userid": userid,
#                 "sender": sender,
#             }
#         )
        
#     async def sendMessage(self, event):
#         print("event ---------------------",event)
#         message = event["message"]
#         userid = event["userid"]
#         sender = event["sender"]
#         await self.send(text_data=json.dumps({"message": message, "sender": sender,"user_id": userid}))
    


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
import asyncio 
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_chat_history()
        for message in messages:
            await self.send_single_message(message)
            print("connection established")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user"]
        sender = text_data_json["sender"]
        print(user_id)

        user = await self.get_user_by_id(user_id)
        print(user,"------------------user----------------")
        room_name = self.room_name
        msg = await self.chat_save(room_name,user,sender, message)

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
                "user_id": user_id,
                "sender":sender
            }
        )
  
    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)   
    
    @database_sync_to_async
    def get_chat_history(self):
        return list(Message.objects.filter(room_name=self.room_name).order_by('timestamp')[:100])
    
    @database_sync_to_async
    def chat_save(self, room_name, user,sender, message):
        message_obj = Message(room_name=room_name, user=user, sender=sender, message=message)
        message_obj.save()


    async def send_single_message(self, message):
        await sync_to_async(self.scope["session"].save)()
        await asyncio.sleep(1)

        await self.send(text_data=json.dumps({
            "message": message.message,
            "user_id": message.user_id,
            "sender" : message.sender
        }))

    async def sendMessage(self, event):
        message = event['message']
        user_id = event['user_id']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            "message": message,
            "user_id": user_id,
            "sender" : sender
        }))













