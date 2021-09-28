from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self,instance):
        product = super().to_representation(instance)
        product['image'] = 'http://localhost:8000/api/product/media/' + product['image']
        return product
