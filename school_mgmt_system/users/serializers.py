from rest_framework import serializers
from django.db import models
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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
        #fields = ('email','password','first_name','last_name','is_staff','is_superuser','is_active')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
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
    """
    Reset Password Email Request Serializer.
    """

    email = serializers.EmailField()

    class Meta:
        fields = ("email",)



class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset Password Serializer.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data