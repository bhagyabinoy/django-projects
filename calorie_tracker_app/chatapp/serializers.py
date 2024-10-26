from rest_framework import serializers
from django.db import models
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class roomSerializers(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

class messageSerializers(serializers.ModelSerializer):

    user = UserSerializer()
    created_on = serializers.DateTimeField(format='%m/%d/%Y %I:%M %p')
    class Meta:
        model = Message
        fields = '__all__'

