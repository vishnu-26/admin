from rest_framework import serializers
from .models import Order,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields='__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

    def to_representation(self,instance):
        order  = super().to_representation(instance)
        order_items = OrderItemSerializer(OrderItem.objects.filter(order=order['id']),many=True).data
        order['total_price'] = sum((order_item['price']*order_item['quantity']) for order_item in order_items)
        order['order_items'] = order_items
        return order
