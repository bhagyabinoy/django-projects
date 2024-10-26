from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']
        






































from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class UpdateSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    #password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    #password2 = serializers.CharField(write_only=True, required=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('first_name','last_name','email','is_staff','is_active', 'is_admin')