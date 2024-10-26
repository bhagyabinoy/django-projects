from django.db import models
from accounts.models import User
import uuid
# Create your models here.



class Product(models.Model):
    product_id = models.CharField(max_length=200, default='defaultvalue')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price_id = models.CharField(max_length=100, null=True, blank=True)
    unit_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user}'s Cart: {self.product.name} (Quantity: {self.quantity})"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_success = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return f"Payment for {self.user} - {self.session_id}"
    

class Orders(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    is_cancelled = models.BooleanField(default=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.order_id} - {self.created_at}"


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.product}"



