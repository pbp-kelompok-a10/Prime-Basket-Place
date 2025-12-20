from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from detail_product.models import Product

User = get_user_model()

class ProductViewsTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',  # Superuser needs an email
            password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',  # Regular user also needs an email
            password='user123'
        )
        
        self.product = Product.objects.create(name='Basketball', price=29.99, user=self.regular_user)

    
    def test_create_product_invalid(self):
        self.client.login(username='user', password='user123')
        response = self.client.post(reverse('dashboard:create_product'), {
            'name': '',
            'price': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_create_product_valid(self):
        self.client.login(username='user', password='user123')
        response = self.client.post(reverse('dashboard:create_product'), {
            'name': 'New Ball',
            'price': 39.99
        })
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(name='New Ball').exists())

    def test_edit_product_valid(self):
        self.client.login(username='user', password='user123')
        response = self.client.post(reverse('dashboard:edit_product', args=[self.product.pk]), {
            'name': 'Updated Basketball',
            'price': 49.99
        })
        self.product.refresh_from_db()
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(self.product.name, 'Basketball')
        self.assertNotEqual(self.product.price, 49.99)

    def test_edit_product_not_owner(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('dashboard:edit_product', args=[self.product.pk]))
        self.assertNotEqual(response.status_code, 302)

    def test_delete_product_valid(self):
        self.client.login(username='user', password='user123')
        response = self.client.delete(reverse('dashboard:delete_product', args=[self.product.pk]))
        self.assertRedirects(response, reverse('dashboard:show_main'))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_delete_product_not_owner(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.delete(reverse('dashboard:delete_product', args=[self.product.pk]))
        self.assertRedirects(response, reverse('dashboard:show_main'))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
