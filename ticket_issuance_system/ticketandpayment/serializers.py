from rest_framework import serializers
from django.db import models
from .models import *
from .djongo_models import *



class pricingSerializers(serializers.ModelSerializer):

    class Meta:
        model = Pricing
        fields = '__all__'


class pricingforeventSerializers(serializers.ModelSerializer):

    class Meta:
        model = Pricing
        fields = ['id','unit_amount']

class paymentSerializers(serializers.ModelSerializer):
   
    class Meta:
        model = Payment
        fields = '__all__'


class TicketCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCollection
        fields = '__all__'