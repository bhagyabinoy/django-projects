from django.shortcuts import render
from .models import Room,Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models  import *

# Create your views here.
def home(request):
    return render(request,'chatpage.html')

class RoomList(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request): 
        queryset = Room.objects.all()
        print(queryset)
        serializer = roomSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MessagesRetrieve(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request,slug): 
        room_name=Room.objects.get(slug=slug).name
        queryset = Message.objects.filter(room=Room.objects.get(slug=slug))
        serializer = messageSerializers(queryset, many=True)
        messages = serializer.data
        data = {"room_name":room_name,"slug":slug,'messages':messages}
        return Response(data, status=status.HTTP_200_OK)

def chatapp_home(request):
    return render(request,"rooms.html")

def chatapp_room(request):
    return render(request,"room.html")   
 

