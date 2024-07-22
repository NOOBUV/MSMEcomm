from psycopg2 import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Product
from .serializers import SellerSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                serialized_user = serializer.data
                return Response({'user': serialized_user}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'access': str(token)}, status=status.HTTP_200_OK)
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
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = Product.objects.get(pk=pk, seller=request.user)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk, seller=request.user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HelloWorldView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("Hello, World!")