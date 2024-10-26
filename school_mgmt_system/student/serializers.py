from rest_framework import serializers
from django.db import models
from .models import *

class StudentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class StudentAttendanceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('student_ID', 'standard', 'division',)

class MarkAttendanceSerializers(serializers.ModelSerializer):
    stud_attendance = StudentAttendanceSerializers(many=True, read_only=True)
    class Meta:
        model = Attendance
        fields = ('student','date', 'markattendance', 'stud_attendance')
        fields = '__all__'