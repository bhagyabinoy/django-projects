from django.db import models
from accounts.models  import *
from food.models import *


def get_all_user_instances():
    return User.objects.all().order_by('id')

def get_all_consumedbyuser_instances():
    return ConsumedByUser.objects.all().order_by('id')

def user_detail(pk):
    return User.objects.get(id=pk)

def consumed_detail(pk):
    return ConsumedByUser.objects.get(id=pk)

def consumed_by_date(user,date):
    return ConsumedByUser.objects.values_list('calories', flat=True).filter(user=user, date=date)

def consumed_by_month(user,month):
    return ConsumedByUser.objects.values_list('calories', flat=True).filter(user=user, date__month=month)

def consumed_by_week(user,week):
    return ConsumedByUser.objects.values_list('calories', flat=True).filter(user=user, date__week=week)

def get_fooddetails_by_name(food_name):
    return FoodItem.objects.filter(name=food_name).values()

def consumedlist_by_date(user,date):
    return ConsumedByUser.objects.all().filter(user=user, date=date).values_list('food','quantity','calories', 'date')

def consumedlist_by_month(user,year, month):
    return ConsumedByUser.objects.all().filter(user=user, date__year=year,date__month=month).values_list('food','quantity','calories', 'date')

def consumedlist_by_week(user,year, week):
    return ConsumedByUser.objects.all().filter(user=user, date__year=year,date__week=week).values_list('food','quantity','calories', 'date')

def get_food_details(name):
    return FoodItem.objects.get(name=name)