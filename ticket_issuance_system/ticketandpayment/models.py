from django.db import models
from userandevent.models import *
from .mongodb_utils import db
# Create your models here.

class AdminModule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='admin_module')
    def __str__(self):
        return str(self.id) + "- " + str(self.user)
    
# mongo database
ticket_collection = db.testingcollection


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    event_booking = models.ForeignKey(EventBookings, on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_date = models.DateField(null=True, blank=True, auto_now=True)
    status = models.IntegerField(default=0)  # 0-Pending,1- Paid, 2- Failed
    
    def __str__(self):
        return str(self.id) + "- " + str(self.user)+ "- " + str(self.event)+ "- " + str(self.status)


class Pricing(models.Model):
    eventpricing_id = models.CharField(max_length=200, default='defaultvalue')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price_id = models.CharField(max_length=100, null=True, blank=True)
    unit_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.id) + '--' + str(self.eventpricing_id) + '--' + str(self.name)+ '--' + str(self.unit_amount)
    

