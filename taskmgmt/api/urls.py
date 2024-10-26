from django.urls import path
from . import views
from .views import *


urlpatterns = [

    path('task/create/',views.add_task, name='task-create'),
    path('department/create/',views.add_department, name='department-create'),
    path('employee/create/',views.add_employee, name='employee-create'),
    path('assigntask/<int:pk>/',views.assign_task, name='assign-task'),
    path('unassigntask/<int:pk>/',views.unassign_task, name='unassign-task'),
    
    path('task/',views.task_list,name = 'task-list'),
    path('department/',views.department_list,name = 'department-list'),
    path('employee/',views.employee_list,name = 'employee-list'),

    path('task/detail/<int:pk>/',views.task_detail,name='task-detail'),
    path('department/detail/<int:pk>/',views.department_detail, name='department-detail'),
    path('employee/detail/<int:pk>/',views.employee_detail,name='employee-detail'),

    path('task/update/<int:pk>/',views.update_task,name='update-task'),
    path('department/update/<int:pk>/',views.update_department, name='update-department'),
    path('employee/update/<int:pk>/',views.update_employee,name='update-employee'),

    path('task/partialupdate/<int:pk>/',views.partialupdate_task,name='partialupdate-task'),
    path('department/partialupdate/<int:pk>/',views.partialupdate_department, name='partialupdate-department'),
    path('employee/partialupdate/<int:pk>/',views.partialupdate_employee,name='partialupdate-employee'),
    
    path('task/delete/<int:pk>/',views.delete_task,name='delete-task'),
    path('department/delete/<int:pk>/',views.delete_department, name='delete-department'),
    path('employee/delete/<int:pk>/',views.delete_employee,name='delete-employee'),

    path('task/bulkcreate/',views.bulk_create_task,name = 'bulk-create-task'),
    path('department/bulkcreate/',views.bulk_create_department,name = 'bulk-create-department'),
    path('employee/bulkcreate/',views.bulk_create_employee,name = 'bulk-create-employee'),

	path('task/bulkupdate/',views.bulk_update_task,name = 'bulk-update-task'),
    path('department/bulkupdate/',views.bulk_update_department,name = 'bulk-update-department'),
    path('employee/bulkupdate/',views.bulk_update_employee,name = 'bulk-update-employee'),
	
    path('task/bulkcreatemany/',views.bulk_create_task_manytrue,name = 'bulk-create-task-manytrue'), 
]