from rest_framework import serializers
from django.db import models
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from ticketandpayment.serializers import pricingforeventSerializers
from datetime import datetime

class userSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class userprofileSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','email',]

class profileSerializers(serializers.ModelSerializer):
    user = userprofileSerializers(required=True)
    class Meta:
        model = Profile
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_data = ret.pop('user')
        ret.update(user_data)
        return ret


class RegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_admin=validated_data['is_admin']
        )
        user.set_password(validated_data['password'])
        user.save()
        print(user, "serializer")
        return user


class PasswordChangeSerializer(serializers.Serializer):

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value
  
    def validate(self, value):
        if value['new_password'] != value['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields does not match."})
        return value


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField()

    def validate(self, data):

        password = data.get("password")
        repeat_password = data.get("repeat_password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields does not match."})
    
        user.set_password(password)
        user.save()
        return data
    
class eventSerializers(serializers.ModelSerializer):

    pricing = pricingforeventSerializers(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['event_start_time']:
            start_time = datetime.strptime(ret['event_start_time'], '%Y-%m-%dT%H:%M:%SZ')
            ret['event_start_time'] = start_time.strftime('%b %d, %Y %I:%M %p')

        if ret['event_end_time']:
            end_time = datetime.strptime(ret['event_end_time'], '%Y-%m-%dT%H:%M:%SZ')
            ret['event_end_time'] = end_time.strftime('%b %d, %Y %I:%M %p')

        return ret
     

class eventbookingdisplaySerializers(serializers.ModelSerializer):

    event = eventSerializers(required=True)
    class Meta:
        model = EventBookings
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        event_data = ret.pop('event')
        ret.update(event_data)
        return ret


class eventbookingSerializers(serializers.ModelSerializer):

    class Meta:
        model = EventBookings
        fields = '__all__'

class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()

class EventSeatStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('id', 'total_seats', 'booked_seats')