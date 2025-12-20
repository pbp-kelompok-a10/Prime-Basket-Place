from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    
    CATEGORY_CHOICES = [
        ('Jersey', 'Jersey'),
        ('Shorts', 'Shorts'),
        ('Hoodie/Sweatshirt', 'Hoodie/Sweatshirt'),
        ('Pants/Tracksuit', 'Pants/Tracksuit'),
        ('Top/T-Shirt', 'Top/T-Shirt'),
        ('Other', 'Apparel (Other)'),
    ]
    
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')
    price = models.IntegerField()
    image_url = models.URLField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self):
        return self.name
    
