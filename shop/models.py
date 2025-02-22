from django.db import models

# Create your models here.
# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()
    photo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name