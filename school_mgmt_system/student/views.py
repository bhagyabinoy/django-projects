from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import View
# Create your views here.



#STUDENT MODEL

def studentview(request):
    return render(request, 'studentlist.html')

#RETRIEVE ALL 

class StudentList(APIView):
    
    def get(self, request):
        items = Student.objects.order_by('student_ID')
        serializer = StudentSerializers(items, many =True)
        studentlist=serializer.data
        return Response(studentlist, status=status.HTTP_200_OK)
        #return render(request,  'studentlist.html', {'studentlist':studentlist}, status=status.HTTP_200_OK)
        #return render(request, studentlist, 'studentlist.html')

def studentcreateview(request):
    return render(request, 'regisstud.html')

class StudentCreate(APIView):

    def post(self, request): 
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            items = Student.objects.order_by('student_ID')
            serializers = StudentSerializers(items, many =True)
            student=serializers.data
            return Response(student, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
#FILTER VIEW   
class StudentFilter(generics.ListAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['standard', 'division','blood_group']

#DETAIL STUDENT

class StudentDetail(APIView):
  
    def get(self,request, pk):
        student = Student.objects.get(student_ID=pk)
        serializer = StudentSerializers(student, many=False)
        studentdetail=serializer.data
        return Response(studentdetail, status=status.HTTP_200_OK)


#STUDENT UPDATE

class UpdateStudent(APIView):
  
    def get(self,request, pk):
        student = Student.objects.get(student_ID=pk)
        serializer = StudentSerializers(student, many=False)
        studentdetail=serializer.data
        return Response(studentdetail, status=status.HTTP_200_OK)

    def patch(self,request, pk):
        student = Student.objects.get(student_ID=pk)
        serializer = StudentSerializers(instance=student, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            items = Student.objects.order_by('student_ID')
            serializers = StudentSerializers(items, many =True)
            student=serializers.data
            return Response(student, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)



#DELETE STUDENT

class DeleteStudent(APIView):
  
    def get(self,request,pk):
        user = Student.objects.get(student_ID=pk)
        user.delete()

        items = Student.objects.order_by('student_ID')
        serializer = StudentSerializers(items, many =True)
        student=serializer.data
        return Response(student, status=status.HTTP_200_OK)
      
#ATTENDANCE MODEL

def attendanceview(request):
    return render(request, 'attendance.html')

#LISTVIEW
class AttendanceList(APIView):

    def get(self, request):
        items = Attendance.objects.order_by('date')
        serializer = MarkAttendanceSerializers(items, many =True)
        attendance=serializer.data
        return Response(attendance, status=status.HTTP_200_OK)

#FILTER VIEW   
class AttendanceFilter(generics.ListAPIView):

    queryset = Attendance.objects.all()
    serializer_class = MarkAttendanceSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

#CREATE VIEW
def markattendanceview(request):
    return render(request, 'markattendance.html')

class AttendanceCreate(APIView):

    def post(self, request): 
        serializer = MarkAttendanceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            items = Attendance.objects.order_by('date')
            serializers = MarkAttendanceSerializers(items, many =True)
            attendance=serializers.data
            print(attendance)
            return Response(attendance, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)


#ATTENDANCE UPDATE

class AttendanceUpdate(APIView):
  
    def get(self,request, pk):
        item = Attendance.objects.get(id=pk)
        serializer = MarkAttendanceSerializers(item, many=False)
        attendance=serializer.data
        return Response(attendance, status=status.HTTP_200_OK)

    def post(self,request, pk):
        item = Attendance.objects.get(id=pk)
        serializer = MarkAttendanceSerializers(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            items = Attendance.objects.order_by('date')
            serializers = MarkAttendanceSerializers(items, many =True)
            attendance=serializers.data
            return Response(attendance, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)



#DELETE ATTENDANCE

class AttendanceDelete(APIView):
  
    def get(self,request,pk):
        user = Attendance.objects.get(id=pk)
        user.delete()

        items = Attendance.objects.order_by('date')
        serializer = MarkAttendanceSerializers(items, many =True)
        attendance=serializer.data
        return Response(attendance, status=status.HTTP_200_OK)


##COUNTER

def dashboardview(request):
    return render(request, 'dashboard.html')

class TotalStudentCounter(APIView):
  
    def get(self,request):
        total_count = Student.objects.count()
        return Response(total_count, status=status.HTTP_200_OK)

class ActiveStudentCounter(APIView):
  
    def get(self,request):
        active_count = Student.objects.filter(isactive='1').count()
        return Response(active_count, status=status.HTTP_200_OK)
