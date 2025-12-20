from django.db import models
from detail_product.models import Product
from django.db.models import Avg

class SliderProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(default=0)

    @property
    def average_rating(self):
        """Menghitung rata-rata rating produk"""
        result = self.product.reviews.aggregate(avg_rating=Avg('rating'))
        return result['avg_rating'] or 0