from django.forms import ModelForm, Textarea
from detail_product.models import Product

class DetailForm(ModelForm):
    class Meta:
        model = Product
        fields = ['description']
        widgets = {
            'description': Textarea(attrs={'rows': 8, 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500'}),
        }