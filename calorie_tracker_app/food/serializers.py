from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
  

    class Meta:
        model =  CategoryModel
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(queryset=CategoryModel.objects.all(),
                                                many=False, allow_null=False, slug_field='category')

    class Meta:
        model = FoodItem
        fields = '__all__'


class FoodsearchSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='category')
    class Meta:
        model = FoodItem
        fields = ('id','name','category','quantity','calories')





