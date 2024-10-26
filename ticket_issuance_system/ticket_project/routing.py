from django.urls import re_path, path
from userandevent import consumers

websocket_urlpatterns = [
    #re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]