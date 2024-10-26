from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeaveModel
from .serializers import LeaveSerializer

class ApplyLeaveView(APIView):
    def post(self, request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteLeaveView(APIView):
    def post(self, request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetriveLeaveView(APIView):
    def post(self, request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApproveLeaveView(APIView):
    def patch(self, request, leave_id):
        try:
            leave = LeaveModel.objects.get(id=leave_id)
        except LeaveModel.DoesNotExist:
            return Response({'error': 'Leave not found.'}, status=status.HTTP_404_NOT_FOUND)

        leave.is_approved = True
        leave.save()
        serializer = LeaveSerializer(leave)
        return Response(serializer.data, status=status.HTTP_200_OK)
