from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.PositiveIntegerField()
    image = models.URLField(null= True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.nombre
