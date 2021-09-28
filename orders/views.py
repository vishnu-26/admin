import json
import time
import csv
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from .models import Order,OrderItem
from products.models import Product
from user.models import User
from .serializers import OrderSerializer,OrderItemSerializer
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from user.authentication import JWTAuthentication,is_authenticated
from user.permissions import has_permission
from .utils import get_orders_details

# Create your views here.

#def get_order_detail(pk):
#    order = list(Order.objects.filter(id= pk).values())[0]
#    
#    order_items = list(OrderItem.objects.filter(id= pk).values())
#    order['total_price'] = sum((order_item['price']*order_item['quantity']) for order_item in order_items)
#    order['order_items'] = order_items
#    return order


@api_view(['GET'])
@is_authenticated
@has_permission
def get_orders(request,**kwargs):
    start = time.time()

#    print(kwargs['user'])
    orders = Order.objects.all()
#    orders = list(orders_queryset.values())
#    print(orders)
#
#    for order in orders:
#        order_items = list(OrderItem.objects.filter(order= order['id']).values())
#        order['total_price'] = sum((order_item['price']*order_item['quantity']) for order_item in order_items)
#        order['order_items'] = order_items

    data = get_orders_details(orders)

    end= time.time()
    print(end-start)
    
    return Response({
        'Orders' : data
    })


@api_view(['GET'])
@is_authenticated
@has_permission
def get_order(request,**kwargs):
    start = time.time()

#    print(request.query_params['order_id'])
    order = Order.objects.filter(id=request.query_params['order_id'])
    data = get_orders_details(order)

    end = time.time()
    print(end-start)
    
    return JsonResponse({
        'Order': data
    })

#@api_view(['GET'])
#@is_authenticated
#def get_user_orders(request,**kwargs):
#    start = time.time()
#    try:
#        orders = Order.objects.filter(customer_id=kwargs['user'])
#        data = get_orders_details(orders)
#
#    except:
#        return JsonResponse({
#            'Error': 'Something went Wrong!!'
#        },status=500)
#
#
#    end=time.time()
#    print(end-start)
#    return JsonResponse({
#            'Orders': data
#    },status=200)

     


@api_view(['GET'])
def export_orders_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'

    r = requests.get(url='http://localhost:8000/api/orders/').json()
    orders= r['Orders']
    
    writer = csv.writer(response)
    writer.writerow(['ID','Customer Id','Shipping Address','Product Id','Price','Quantity'])

    for order in orders:
#        writer.writerow([order['id'],order['customer_id'],order['delivery_address'],'','',''])
        
        for order_item in order['order_items']:
            writer.writerow([
                            order['id'],
                            order['customer_id'],
                            order['delivery_address'],
                            order_item['product_id'],
                            order_item['price'],
                            order_item['quantity']
                           ])
    
    return response



#def get_orderitem(pk):
#    order = list(Order.objects.filter(id= pk).values())[0]
#    
#    order_items = list(OrderItem.objects.filter(id= pk).values())
#    order['total_price'] = sum((order_item['price']*order_item['quantity']) for order_item in order_items)
#    order['order_items'] = order_items
#    return order



#@api_view(['GET'])
#def orders(request):
#    start = time.time()
#
#    serializer = OrderSerializer(Order.objects.all(),many=True).data
#    
#    end = time.time()
#    print(end-start)
#
#    return JsonResponse({
#        'Orders' : serializer
#    })



#@api_view(['POST'])
#def create_order(request):
#    start = time.time()
#    
#    serializer = OrderSerializer(data=request.data)
#    serializer.is_valid(raise_exception=True)
#    serializer.save()
#    
#    end = time.time()
#    print(end-start)
#    
#    return Response({
#        'Order' : serializer.data
#    })



@api_view(['POST'])
def create_order(request):
    start = time.time()
    
    
    _customer = User.objects.get(user_id = request.data.get('customer'))
    _order = Order.objects.create(
                customer = _customer,
                delivery_address = request.data.get('delivery_address')
             )

    order = get_order_detail(_order.id)
    end = time.time()
    print(end-start)
    
    return JsonResponse({
        'Order' : order
    })


#@api_view(['GET'])
#def get_order(request,pk):
#    start = time.time()
#
#    data = get_order_detail(pk)
#
#    end = time.time()
#    print(end-start)
#    
#    return JsonResponse({
#        'Order': data
#    }) 

    


@api_view(['POST'])
def create_order_item(request):
    start = time.time()

    _product = Product.objects.get(id= request.data.get('product'))
    _order = Order.objects.get(id= request.data.get('order'))
    order_item = OrderItem.objects.create(
                        product= _product,
                        price= request.data.get('price'),
                        quantity= request.data.get('quantity'),
                        order= _order
                  )
    end = time.time()
    print(end-start)


    return JsonResponse({
        'Order_Item': order_item.id
    })



#@api_view(['POST'])
#def create_order_item(request):
#    start = time.time()
#
#    serializer = OrderItemSerializer(data=request.data)
#    serializer.is_valid(raise_exception=True)
#    serializer.save()
#
#    end = time.time()
#    print(end-start)
#    
#    return Response({
#        'Order_Item' : serializer.data
#    })


@api_view(['GET'])
def chart_api_view(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DATE_FORMAT(o.created_at, '%Y-%m-%d') as date , sum(i.price*i.quantity) as sum
            FROM orders_order as o
            JOIN orders_orderitem as i ON o.id=i.order_id
            GROUP BY date
        ''')

        row = cursor.fetchall()

    data = [{'date':result[0],'Total Money':result[1]} for result in row]

    return Response({
        'data': data
    })















