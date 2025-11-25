from django.db import models
from .customer import Customer

class Store(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="store"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "store"
        verbose_name_plural = "stores"
