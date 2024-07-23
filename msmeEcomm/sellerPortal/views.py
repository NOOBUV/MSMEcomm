import logging

logger = logging.getLogger(__name__)

from psycopg2 import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Product
from .serializers import SellerSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError
import pandas as pd
from .tasks import generate_product_summaries

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                serialized_user = serializer.data
                logger.info(f"User {serialized_user['email']} signed up successfully.")
                return Response({'user': serialized_user}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                logger.error("User with this email already exists.")
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Signup failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"User {email} logged in successfully.")
            return Response({'access': str(token)}, status=status.HTTP_200_OK)
        logger.error(f"Login failed for user {email}.")
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk = None):
        if pk:
            product = Product.objects.get(pk=pk, seller=request.user)
            serializer = ProductSerializer(product)
        else:
            products = Product.objects.filter(seller=request.user)
            serializer = ProductSerializer(products, many=True)
        logger.info(f"Products retrieved for user {request.user.email}.")
        return Response(serializer.data)

    def post(self, request):
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            try:
                df = pd.read_csv(csv_file)
                products = []
                for _, row in df.iterrows():
                    try:
                        product_data = {
                            'seller': request.user,
                            'name': row['name'],
                            'price': row['price'],
                            'stock': row['stock']
                        }
                        
                        if 'description' in row and row['description'] and row['description'].lower() != 'nan':
                            product_data['description'] = row['description']
                        
                        product = Product(**product_data)
                        product.save()
                        products.append(product)
                    except ValidationError as e:
                        logger.error(f"CSV file validation error: {e}")
                        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                generate_product_summaries.delay()  # Enqueue the task
                logger.info(f"CSV file processed successfully for user {request.user.email}.")
                return Response({'status': 'CSV file processed successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error processing CSV file: {e}")
                return Response({'error': 'Error processing file'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProductSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                product = serializer.save()
                generate_product_summaries.delay()  # Enqueue the task
                logger.info(f"Product created successfully for user {request.user.email}.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f"Product creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = Product.objects.get(pk=pk, seller=request.user)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Product {pk} updated successfully for user {request.user.email}.")
            return Response(serializer.data)
        logger.error(f"Product update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk, seller=request.user)
        product.delete()
        logger.info(f"Product {pk} deleted successfully for user {request.user.email}.")
        return Response(status=status.HTTP_204_NO_CONTENT)

class HelloWorldView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("Hello, World!")