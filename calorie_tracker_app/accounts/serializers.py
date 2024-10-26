from rest_framework import serializers
from django.db import models
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


class userSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


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
            is_staff=validated_data['is_staff']
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


class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()


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
    

class AddCaloriesConsumedSerializer(serializers.ModelSerializer):

    food = serializers.SlugRelatedField(queryset=FoodItem.objects.all(),
                                                many=False, allow_null=False, slug_field='name')

    class Meta:
        model = ConsumedByUser
        fields = ('user','food','quantity','calories','date')


class CaloriesConsumedSerializer(serializers.ModelSerializer):
    food = serializers.SlugRelatedField(queryset=FoodItem.objects.all(),
                                                many=False, allow_null=False, slug_field='name')          
    class Meta:
        model = ConsumedByUser
        fields = ('food','quantity','calories', 'date')