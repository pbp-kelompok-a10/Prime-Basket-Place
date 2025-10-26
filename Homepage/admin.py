from django.contrib import admin
from .models import SliderProduct
from .forms import SliderProductForm

@admin.register(SliderProduct)
class SliderProductAdmin(admin.ModelAdmin):
    form = SliderProductForm
    list_display = ('product', 'is_featured', 'discount', 'average_rating_display')
    list_filter = ('is_featured',)
    search_fields = ('product__name',)
    list_editable = ('is_featured', 'discount')

    def average_rating_display(self, obj):
        return f"{obj.average_rating:.1f}"
    average_rating_display.short_description = "Avg Rating"

