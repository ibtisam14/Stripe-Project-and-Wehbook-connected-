from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to="product/image", blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} --> {self.price}"
    
    def get_absolute_url(self):
        return reverse("core:detail", args=[self.id])


class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    stripe_id = models.CharField(max_length=255)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}--->{self.amount}--->{self.stripe_id}"