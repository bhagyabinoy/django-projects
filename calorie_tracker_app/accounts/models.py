from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from food.models import FoodItem



# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    premium_member = models.BooleanField(default=False)
    plan = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    


class ConsumedByUser(models.Model):

    user = models.ForeignKey(User, blank=True,on_delete=models.CASCADE, related_name = 'user_food')
    food = models.ForeignKey(FoodItem,blank=True,on_delete=models.CASCADE, related_name='food_consumed')
    quantity = models.FloatField(null=True, blank=True)
    calories = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True)







