from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Seller
from rest_framework.authtoken.models import Token

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