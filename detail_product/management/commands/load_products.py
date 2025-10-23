import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from detail_product.models import Product
from pathlib import Path

class Command(BaseCommand):
    help = 'Loads products from basketball.json into the database'

    def handle(self, *args, **kwargs):
        # 1. Clear old products to avoid duplicates.
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared old products.'))

        # 2. Find a superuser to be the default owner of the products.
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.ERROR('No superuser found. Please run "python manage.py createsuperuser" first.'))
            return

        # 3. **FIXED PATH**: Define the correct relative path to the JSON file.
        # This path goes up from the command's location to the project root,
        # then into the 'prime_basket_place/fixtures/' directory.
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        json_path = base_dir / 'prime_basket_place' / 'fixtures' / 'basketball.json'

        if not json_path.exists():
            self.stdout.write(self.style.ERROR(f'File not found at the expected path: {json_path}'))
            return

        # 4. Open and read the JSON file.
        with open(json_path, 'r') as f:
            data = json.load(f)

        # 5. Loop through the data and create Product objects.
        # This part correctly handles the new JSON structure you provided.
        for item in data:
            Product.objects.create(
                user=user,
                name=item.get('product_name'),
                brand=item.get('brand'),
                category=item.get('category'), # Using the correct 'category' key
                price=item.get('price_idr'),
                image_url=item.get('image_url')
                # Description is intentionally left null by default.
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(data)} products into the database.'))