from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.PositiveIntegerField()
    image = models.URLField(null= True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def total(self):
        items = self.items.all()
        if not items:
            return 0
        return sum(item.total_price() for item in items)
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
