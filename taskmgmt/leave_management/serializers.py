from rest_framework import serializers
from .models import LeaveModel

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveModel
        fields = '__all__'
