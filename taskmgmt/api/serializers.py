from django.db.models import fields
from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):

    employees_assigned = serializers.StringRelatedField(many=True, allow_null=True, read_only=True)	
    class Meta:
        model = TaskModel
        fields = ('id','task_name', 'description','startdate','enddate','employees_assigned')
        

class DepartmentSerializer(serializers.ModelSerializer):

    #employ_dept = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    employ_dept = serializers.StringRelatedField(many=True, allow_null=True, read_only=True)
    class Meta:
        model = DepartmentModel
        fields = ('id','department','employ_dept')


class EmployeeSerializer(serializers.ModelSerializer):
        
    department = serializers.SlugRelatedField(queryset=DepartmentModel.objects.all(),
                                                many=False, allow_null=True, slug_field='department')	
            
    class Meta:
        model = EmployeeModel
        fields = ('emp_id','first_name','last_name', 'emp_img','department','contact_num','tasks')

class AssignTaskSerializer(serializers.ModelSerializer):

           
    class Meta:
        model = EmployeeModel
        fields = ('emp_id','tasks')

class UnassignTaskSerializer(serializers.ModelSerializer):

           
    class Meta:
        model = EmployeeModel
        fields = ('emp_id','tasks')
