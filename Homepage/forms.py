from django.forms import ModelForm
from .models import SliderProduct

class SliderProductForm(ModelForm):
    class Meta:
        model = SliderProduct
        fields = [
            "is_featured",
            "discount",
        ]