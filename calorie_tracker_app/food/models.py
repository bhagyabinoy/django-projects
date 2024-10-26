from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
 

class CategoryModel(models.Model):
    category = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return '%s' %(self.category)


class FoodItem(models.Model):
    name= models.CharField(max_length=40, unique=True, validators=[RegexValidator('[+-/%]', inverse_match=True)])
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=100)
    calories= models.IntegerField(default=100)

    def __str__(self):
        return '%s %s %s' %(self.name, self.quantity, self.calories)