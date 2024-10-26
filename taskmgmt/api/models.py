from django.db import models
from django.forms import IntegerField

# Create your models here.

class TaskModel(models.Model):

	task_name= models.CharField(max_length = 100, null = True, blank=True)
	description = models.TextField(null = True, blank=True)
	startdate = models.DateField(null = True, blank=True)
	enddate = models.DateField(null = True, blank=True)
	
	def __str__(self):
	 	return self.task_name

class DepartmentModel(models.Model):

	department = models.CharField(max_length = 100)
    
	def __str__(self):
	    return self.department


class EmployeeModel(models.Model):

    emp_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length = 50, null = True, blank=True)
    last_name = models.CharField(max_length = 50, null = True, blank=True)
    emp_img = models.ImageField(null = True, blank=True)
    contact_num = models.IntegerField(null = True, blank=True)
    level = models.CharField(max_length = 50, null = True, blank=True)
    designation = models.CharField(max_length = 50, null = True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    highest_education = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    department = models.ForeignKey(DepartmentModel, null=False, blank=True,
	             on_delete = models.CASCADE,related_name = 'employ_dept')
    tasks = models.ManyToManyField(TaskModel,related_name='employees_assigned',blank=True)
    
	
    def __str__(self):
	    return "%s %s" % (self.first_name, self.last_name)

       