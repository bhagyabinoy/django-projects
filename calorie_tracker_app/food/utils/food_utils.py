from accounts.models  import *
from food.models import *


def get_all_food_item_instances():
    return FoodItem.objects.all().order_by('id')

def get_all_category_instances():
    return CategoryModel.objects.all().order_by('id')

def food_detail(pk):
    return FoodItem.objects.get(id=pk)

def category_detail(pk):
    return CategoryModel.objects.get(id=pk)

def filter_veg():
    return FoodItem.objects.filter(category_id=1)

def filter_nonveg():
    return FoodItem.objects.filter(category_id=2)

def calories_lt_100():
    return FoodItem.objects.all().filter(calories__lt=100)

def calories_gt_300():
    return FoodItem.objects.all().filter(calories__gt=300)

def calories_range():
    return FoodItem.objects.all().filter(calories__range=(100, 200))