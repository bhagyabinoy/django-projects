from food.models import FoodItem
from rest_framework import status
from rest_framework.response import Response
from .models import *
from accounts.serializers import *
from food.serializers import *


class FilterMixins:

    def __init__(self):
        pass


    def consumed_by_date_mixin(self,date, user):

        if date is None and  user is None:
            return Response("no input received", status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = ConsumedByUser.objects.filter(user=user, date=date)
            if queryset.count() == 0:		
                return Response("no records found", status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = CaloriesConsumedSerializer(queryset, many=True)
                consumed_list=serializer.data
                print(consumed_list)
                return consumed_list


    def consumed_by_week_mixin(self,week,year,user):
       
        if week is None: 
            return Response("Please enter a valid week number", status=status.HTTP_400_BAD_REQUEST)
        elif year is None: 
            return Response("Enter the year", status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = ConsumedByUser.objects.filter(user=user, date__year=year,date__week=week)
            print(queryset)
            if queryset.count() == 0:		
                return Response("no records found", status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = CaloriesConsumedSerializer(queryset, many=True)
                consumed_list=serializer.data
                print(consumed_list)
                return consumed_list
            

    def consumed_by_month_mixin(self,month, year, user):

        if month is None: 
            return Response("Please enter month", status=status.HTTP_400_BAD_REQUEST)
        elif year is None: 
            return Response("Enter the year", status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = ConsumedByUser.objects.filter(user=user, date__year=year,date__month=month)
            if queryset.count() == 0:	
                return Response("no records found", status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = CaloriesConsumedSerializer(queryset, many=True)
                consumed_list=serializer.data
                print(consumed_list)
                return consumed_list
            
