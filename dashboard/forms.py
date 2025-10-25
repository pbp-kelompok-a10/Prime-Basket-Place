from detail_product.models import Product
from django.forms import ModelForm, Textarea

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "brand", "category", "price", "image_url", "description"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-purple focus:outline-none',
                'placeholder': f'Enter {field.label}'
            })