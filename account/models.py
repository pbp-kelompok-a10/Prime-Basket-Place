from django.db import models
from django.contrib.auth.models import User
from detail_product.models import Product

class Account(models.Model):
    ROLE = [
        ('User', 'User'),
        ('Admin', 'Admin')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    nickname = models.CharField(max_length=30, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)  # simpan URL gambar
    favorites = models.ManyToManyField(Product, related_name='favorited_by', blank=True)
    roles = models.CharField(choices=ROLE, default='User', max_length=10)

    def __str__(self):
        return self.nickname or self.user.username
    
    def is_admin(self):
        return self.roles == 'Admin'
