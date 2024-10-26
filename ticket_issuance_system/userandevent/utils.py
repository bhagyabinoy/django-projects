from .models  import *


def get_all_user_instances():
    return User.objects.all()

def user_detail(pk):
    return User.objects.get(id=pk)

def get_all_profile_instances():
    return Profile.objects.all().order_by('-id')

def profile_detail(pk):
    return Profile.objects.get(id=pk)

def get_all_event_instances():
    return Event.objects.all().order_by('id')

def event_detail(pk):
    return Event.objects.get(id=pk)

def get_all_eventbooking_instances():
    return EventBookings.objects.all().order_by('-id')

def eventbooking_detail(pk):
    return EventBookings.objects.get(id=pk)

