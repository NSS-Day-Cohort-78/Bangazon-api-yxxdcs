from django.db import models
from .customer import Customer
from .product import Product

class Like(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        """Customer can only like a product once"""
        unique_together = ('customer', 'product')
