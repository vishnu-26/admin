from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from user.authentication import JWTAuthentication
from user.permissions import IsAuthenticated
from .models import Product
from .utils import upload_file
from .serializers import ProductSerializer

# Create your views here.

@api_view(['GET'])
def get_products(request):
    try:
        product_serializer = ProductSerializer(Product.objects.all(),many=True).data
        message = 'Success'
        status=200
    except:
        product_serializer=None
        message='Some Error Occurred'
        status=500

    return Response({
        'Products' : product_serializer
    },status=status)



@api_view(['POST'])
def upload_product(request):
    
    image = request.data['image']
    request.data['image'] = image.name
    
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid()
    serializer.save()

    upload_file(image)
    
    return Response({
        'Product':serializer.data
    },status=201)



    





 






