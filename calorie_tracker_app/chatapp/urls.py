from django.urls import path
from .views import *
from .routing import *


urlpatterns = [

    path('roomslist/', RoomList.as_view(), name='room-list'),
    path('messages/<slug:slug>/', MessagesRetrieve.as_view(), name='messages-retrieve'),

    #template urls
    path('room/',chatapp_room, name='chatapp_room'),
    path('chatapp_home/',chatapp_home, name='chatapp_home')
]
urlpatterns += websocket_urlpatterns