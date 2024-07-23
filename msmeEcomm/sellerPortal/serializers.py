from rest_framework import serializers
from .models import Seller, Product
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['email', 'name', 'specialization', 'niche', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        seller = super().create(validated_data)
        logger.info(f"Seller {seller.email} created successfully.")
        return seller

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'seller': {'required': False}}

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        product = super().create(validated_data)
        logger.info(f"Product {product.name} created successfully for seller {product.seller.email}.")
        return product
    