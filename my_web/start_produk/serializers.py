from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'identifier', 'unit', 'quantity', 'price',
                  'status', 'created_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'identifier', 'category', 'unit', 'quantity', 'price', 'status']

    def validate(self, data):
        """
        Ensure product quantity and price are greater than zero before creation.
        """
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        if data['price'] <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return data


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'identifier', 'category', 'unit', 'quantity', 'price', 'status', 'is_archived']

    def validate(self, data):
        """
        Ensure product quantity and price are greater than zero before updating.
        """
        if 'quantity' in data and data['quantity'] <= 0:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return data


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ['id', 'full_name', 'region', 'inn', 'address_registration', 'address_residence',
                  'passport_series', 'passport_number', 'passport_issued_by', 'passport_issue_date',
                  'passport_expiry_date', 'phone_number_1', 'phone_number_2', 'photo', 'is_archived',
                  'created_at', 'updated_at']


class SalesHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = SalesHistory
        fields = ['id', 'distributor', 'product', 'unique_code', 'unit', 'quantity', 'sale_date', 'total_sum']


class ReturnHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ReturnHistory
        fields = ['id', 'distributor', 'product', 'unique_code', 'unit', 'quantity', 'return_date', 'return_status', 'total_sum']


class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'distributor', 'invoice_number', 'created_at', 'total_amount', 'items']
