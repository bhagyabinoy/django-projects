from django.db import models

# Create your models here.
from api.models import EmployeeModel

class LeaveModel(models.Model):
    LEAVE_TYPES = (
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('lop', 'Loss of Payment'),
    )

    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"
