from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
#from ticketandpayment.models import Pricing
# Create your models here.


#class UserManager(BaseUserManager):
    # def _create_user(self, email, password, **extra_fields):
    #     if not email:
    #         raise ValueError('The Email field must be set')
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_admin', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_admin', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #objects = UserManager()

    def __str__(self):
        return str(self.id) + "- " + self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "- " + str(self.user.first_name) + ' ' + str(self.user.last_name)



class Event(models.Model):

    event_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    total_seats = models.IntegerField(default=100)
    event_start_time = models.DateTimeField(null=True, blank=True)
    event_end_time = models.DateTimeField(null=True, blank=True)
    booked_seats = models.JSONField(null=True, blank=True)
    pricing = models.ManyToManyField('ticketandpayment.Pricing', related_name='events')

    def __str__(self):
        return str(self.id) + '--' + str(self.event_name) + '--' + str(self.event_start_time) + '--' + str(self.event_end_time) + '--' + str(self.total_seats) + '--' + str(self.booked_seats)
    

class EventBookings(models.Model):

    user = models.ForeignKey(User, blank=True,on_delete=models.CASCADE, related_name = 'user_eventbooking')
    event = models.ForeignKey(Event, blank=True,on_delete=models.CASCADE, related_name = 'event_booking')
    booking_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    seats_booked = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return str(self.user) + '--' + str(self.id) + '--' + str(self.event) + '--' + str(self.booking_date)+ '--' + str(self.seats_booked)



class Message(models.Model):
    room_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.room_name) + '--' + str(self.user) +'--' + str(self.sender) + '--' + str(self.message) + '--' + str(self.timestamp)
