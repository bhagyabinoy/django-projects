from django.urls import path
from . import consumers
from django.urls import path , include,re_path
from .consumers import ChatConsumer

# websocket_urlpatterns = [
#     path('ws/chat/', consumers.ChatConsumer.as_asgi()),
# ]
websocket_urlpatterns = [
	#path("<room_slug>" , ChatConsumer.as_asgi()) ,
    re_path(r'ws/chat/(?P<room_slug>[\w-]+)/$', ChatConsumer.as_asgi()),
]