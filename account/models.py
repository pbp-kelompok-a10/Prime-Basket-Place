from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    nickname = models.CharField(max_length=30, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)  # simpan URL gambar
    # favorites = models.ManyToManyField(Product, related_name='favorited_by', blank=True)


    def __str__(self):
        return self.nickname or self.user.username
