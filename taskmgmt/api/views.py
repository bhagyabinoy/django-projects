from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

from django.http import HttpResponse
from django.template import loader



"""CREATE"""

#task
@api_view(['POST'])
def add_task(request):

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#department
@api_view(['POST'])
def add_department(request):

    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#employee
@api_view(['POST'])
def add_employee(request):

    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


"""RETRIEVE VIEW"""
"""List View"""
#task_list
@api_view(['GET'])
def task_list(request):

    task = TaskModel.objects.all()
    serializer = TaskSerializer(task, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
#department_list
@api_view(['GET'])
def department_list(request):

    department = DepartmentModel.objects.all()
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#employee_list
@api_view(['GET'])
def employee_list(request):

    employee = EmployeeModel.objects.all()
    serializer = EmployeeSerializer(employee, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

"""Detail View"""

#task_detail
@api_view(['GET'])
def task_detail(request,pk):

    task = TaskModel.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

  
#department_detail

@api_view(['GET'])
def department_detail(request,pk):
    department = DepartmentModel.objects.get(id=pk)
    serializer = DepartmentSerializer(department, many=False)
    return Response(serializer.data)

#employee_detail
@api_view(['GET'])
def employee_detail(request,pk):

    employee = EmployeeModel.objects.get(emp_id=pk)
    serializer = EmployeeSerializer(employee, many=False)
    return Response(serializer.data)


"""UPDATE VIEW"""

#task_update

@api_view(['PUT'])
def update_task(request, pk):
    task = TaskModel.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    
    if serializer.is_valid():
        serializer.save()
        #print(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


#department_update
@api_view(['PUT'])
def update_department(request, pk):
    department= DepartmentModel.objects.get(id=pk)
    serializer  = DepartmentSerializer(instance=department, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


#employee_update
@api_view(['PUT'])
def update_employee(request, pk):
    employee = EmployeeModel.objects.get(emp_id=pk)
    serializer= EmployeeSerializer(instance=employee, data=request.data)
    #serializer1= EmployeeViewSerializer(instance=employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        #print(serializer.data)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


"""PARTIAL UPDATE VIEW"""

#task_partialupdate

@api_view(['PATCH'])
def partialupdate_task(request, pk):
    task = TaskModel.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data,partial=True)

    
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


#department_partialupdate
@api_view(['PATCH'])
def partialupdate_department(request, pk):
    department= DepartmentModel.objects.get(id=pk)
    serializer  = DepartmentSerializer(instance=department, data=request.data,partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


#employee_partialupdate
@api_view(['PATCH'])
def partialupdate_employee(request, pk):
    employee = EmployeeModel.objects.get(emp_id=pk)
    serializer= EmployeeSerializer(instance=employee, data=request.data,partial=True)
    
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


"""DELETE"""

#task_delete
@api_view(['DELETE'])
def delete_task(request, pk):
    task = TaskModel.objects.get(id=pk)
    task.delete()
    return Response("Task deleted successfully", status=status.HTTP_204_NO_CONTENT)

#department_delete
@api_view(['DELETE'])
def delete_department(request, pk):
    department = DepartmentModel.objects.get(id=pk)
    department.delete()
    return Response("Department deleted successfully", status=status.HTTP_204_NO_CONTENT)

#employee_delete
@api_view(['DELETE'])
def delete_employee(request, pk):
    employee = EmployeeModel.objects.get(emp_id=pk)
    employee.delete()
    return Response("Employee deleted successfully", status=status.HTTP_204_NO_CONTENT)



"""ASSIGNING AND UNASSIGNING TASKS"""


#assigntask
@api_view(['PATCH'])
def assign_task(request,pk):

    employee = EmployeeModel.objects.get(emp_id=pk)
    task=request.data.get('tasks')
    #print(type(Task))
    print(task)
    #  taskone=TaskModel.objects.get(id=1)
    #  employee.tasks.add(taskone)
    #print(employee.tasks.all())        #prints already assigned tasks
    task_query=list(set(employee.tasks.all().values_list('id', flat=True)))
    print(task_query)       # returns already assigned tasks
    #print(type(task_query))      # returns queryset type
    #tasks_list = list(task_query)       # queryset to a python's list type
    #print(tasks_list)
    #print(type(tasks_list))     #returns list type
    task_list=[]
    for i in task:
        if i in task_query:
            continue
        else:
            #employee.tasks.add(i)
            #print(employee.tasks.all())
            #return Response("New task assigned successfully",status=status.HTTP_202_ACCEPTED)  

            task_list.append(i)
    for i in task_list:
        employee.tasks.add(i)
    #print(employee.tasks.all()) 
                  
    serializer = EmployeeSerializer(employee, many=False)
    return Response(serializer.data)
    

#unassigntask
@api_view(['PATCH'])
def unassign_task(request,pk):

    employee = EmployeeModel.objects.get(emp_id=pk)
    task=request.data.get('tasks')
    print(task)
    task_query=list(set(employee.tasks.all().values_list('id', flat=True)))
    print(task_query)  

    for i in task:
        if i in task_query:
            employee.tasks.remove(i)
            print(employee.tasks.all()) 
            #return Response("Task unassigned successfully",status=status.HTTP_202_ACCEPTED)

        else:
            continue
    serializer = EmployeeSerializer(employee, many=False)
    return Response(serializer.data)



"""BULK CREATE"""

#bulk_create_task

@api_view(['POST'])
def bulk_create_task(request):

    bulk_request = request.data
    bulk_data=[]       
    for i in bulk_request:
        bulk_task = TaskModel(task_name=i.get("task_name"),description=i.get("description"),startdate=i.get("startdate"),enddate=i.get("enddate"))
        bulk_data.append(bulk_task)
    TaskModel.objects.bulk_create(bulk_data)

    #to view
    task = TaskModel.objects.all().order_by('-id')
    serializer = TaskSerializer(task, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)


#bulk_create_department

@api_view(['POST'])
def bulk_create_department(request):

    bulk_request = request.data

    bulk_data=[]        
    for i in bulk_request:
        bulk_dept = DepartmentModel(department=i.get("department"))
        bulk_data.append(bulk_dept)
    DepartmentModel.objects.bulk_create(bulk_data)

    #to view
 
    department = DepartmentModel.objects.all().order_by('-id')
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#bulk_create_employee

@api_view(['POST'])
def bulk_create_employee(request):

    bulk_request = request.data

    employee_task_relationship=EmployeeModel.tasks.through
    print(employee_task_relationship,"#######")

    bulk_data=[]        
    for i in bulk_request:
        bulk_emp = employee_task_relationship(tasks=i.get("tasks")) 
        bulk_data.append(bulk_emp)
    employee_task_relationship.objects.bulk_create(bulk_data)

    # bulk_data=[]        
    # for i in bulk_request:
    #     bulk_emp = EmployeeModel(emp_id=i.get("emp_id"),first_name=i.get("first_name"),last_name=i.get("last_name"),emp_img=i.get("emp_img"),department=i.get("department"),contact_num=i.get("contact_num")) 
    #     bulk_data.append(bulk_emp)
    # EmployeeModel.objects.bulk_create(bulk_data)

    #to view
    employee = EmployeeModel.objects.all()
    serializer = EmployeeSerializer(employee, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


"""BULK UPDATE"""

#bulk_update_task

@api_view(['POST'])
def bulk_update_task(request):

    bulk_task=[]
    bulk_request = request.data

    print(type(bulk_request))
    #print(bulk_request)
    
    for x in bulk_request:          #accessing list items
        print(x, "$$$$")
        key_list = list(x.keys())
        val_list = list(x.values())
        print(key_list,"^^^^^^^^^^^")
        print(val_list)
        TaskModel.objects.filter(pk__in=[4,5]).update(task_name=x.get("task_name"),description=x.get("description"),startdate=x.get("startdate"),enddate=x.get("enddate"))
     

    #print(len(val_list))

    # for x in bulk_request:     
    #     for key,value in x:        # for x in bulk_request:     
    #         print(key,"####")
    #         print(value,"#################")
 
   
    
    # bulk_task = TaskModel.objects.filter(id=key).update()
    #     bulk_task.task_name = value
    #     bulk_task.description = value
    #     bulk_data.append(bulk_task)
    # TaskModel.objects.update(bulk_data, ['task_name','description', 'startdate','enddate'])   
    #use .update..   list of dictionaries
    ##ValueError at /api/task/bulkupdate/    too many values to unpack (expected 2)

    #to view
    task = TaskModel.objects.all().order_by('-id')
    serializer = TaskSerializer(task, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)


#bulk_update_department

@api_view(['POST'])
def bulk_update_department(request):

    bulk_data=[ ]
    bulk_request = request.data

    print(type(bulk_request))
    print(bulk_request)    
    print(bulk_request[0])      #accessing the values     


    for key,value in bulk_request.items():
        print(key,"##")
        print(value,"###")

        dept = DepartmentModel.objects.get(id=key)
        dept.department = value
        bulk_data.append(dept)
    DepartmentModel.objects.bulk_update(bulk_data, ['department'])

    #to view
    department = DepartmentModel.objects.order_by('-id')
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)


#bulk_update_employee

@api_view(['POST'])
def bulk_update_employee(request):

    bulk_data=[]
    bulk_request = request.data

    employee_task_relationship=EmployeeModel.tasks.through
    print(employee_task_relationship)
    for key,value in bulk_request.items():
        #bulk_emp = EmployeeModel(emp_id=i.get("emp_id"),first_name=i.get("first_name"),last_name=i.get("last_name"),emp_img=i.get("emp_img"),department=i.get("department"),contact_num=i.get("contact_num"),tasks=i.get("tasks"))
        bulk_emp = EmployeeModel.objects.get(emp_id=key)
        bulk_emp.first_name = value
        bulk_data.append(bulk_emp)
    EmployeeModel.objects.bulk_update(bulk_data,['first_name'])

    #to view
    employee = EmployeeModel.objects.all().order_by('-emp_id')
    serializer = EmployeeSerializer(employee, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)


#bulk create task with many=true

@api_view(['POST'])
def bulk_create_task_manytrue(request):

    serializer = TaskSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

