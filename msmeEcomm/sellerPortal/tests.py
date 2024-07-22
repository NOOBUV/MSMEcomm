from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Seller, Product
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User  # Import User model

class SellerTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.hello_url = reverse('hello-world')
        self.user_data = {
            'email': 'testing@example.com',
            'name': 'Test User',
            'specialization': 'Test Specialization',
            'niche': 'Test Niche',
            'password': 'testpassword123'
        }
        self.user = Seller.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name'],
            specialization=self.user_data['specialization'],
            niche=self.user_data['niche']
        )
        self.token = Token.objects.create(user=self.user)

    def test_signup(self):
        # Test duplicate signup
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0].code, 'unique')
        user = Seller.objects.get(email=self.user_data['email'])
        user.delete()

        # Test new signup
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)

    def test_login(self):
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_hello_world_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.hello_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Hello, World!")

    def test_hello_world_unauthenticated(self):
        response = self.client.get(self.hello_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProductViewTests(APITestCase):
    def setUp(self):
        self.seller = Seller.objects.create_user(
            email='testuser@example.com',
            password='password123',
            name='Test User',
            specialization='Test Specialization',
            niche='Test Niche'
        )
        self.token = Token.objects.create(user=self.seller)
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.99,
            stock=5,
            seller=self.seller
        )

    def test_get_product(self):
        url = reverse('product', kwargs={'pk': self.product.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 9.99,
            'stock': 10
        }
        url = reverse('products')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product(self):
        url = reverse('product', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 12.99,
            'stock': 15
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        url = reverse('product', kwargs={'pk': self.product.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)