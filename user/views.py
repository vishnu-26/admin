import time
from user.authentication import generate_token
from .authentication import generate_token
from rest_framework import serializers,viewsets,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsAuthenticated
# Create your views here.
from .models import User,Role,Permission
from .serializers import UserSerializer,RoleSerializer,PermissionSerializer
#import bcrypt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
import json
from .authentication import JWTAuthentication,is_authenticated
from .utils import get_user
from orders.models import Order,OrderItem
from orders.utils import get_orders_details



@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['confirm_password']:
        raise APIException('Passwords do not match')

    # hashed_password=bcrypt.hashpw(data['password'].encode("utf-8"),bcrypt.gensalt())
    # data['password']=hashed_password

    try:
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        user_serializer = serializer.data
        print(user_serializer)
        message='Success'
        status=201
    except:
        user_serializer=None
        message='Some Error Occured'
        status = 500
#    
    return JsonResponse(
        {'user':user_serializer,'message':message},status=status
    )


@api_view(['POST'])
def login(request):
    user_id=request.data['user_id']
    password = request.data['password']

    user_serializer = None
    token=None
    try:
        user = User.objects.filter(user_id=user_id).first()
        
        if user:
            if check_password(password,user.password):
                token=generate_token(user)
                message='Login successfull'
                print("Token:",token)
                user_serializer = UserSerializer(user,many=False).data
            else:
                message='Invalid Password'
             
        else:
            message='Invalid Username'
    except:
        message='Something went wrong!!'

       
    return JsonResponse(
        {"user": user_serializer,"token": token,'message':message}
    )


#def get_user(user):
#    try:
#        user_serializer=UserSerializer(user,many=False).data
#        _role = Role.objects.get(id=user_serializer['role'])
#        user_serializer['role']=_role.name
#        role_serializer = RoleSerializer(_role).data
#       print(role_serializer.permissions)
#        user_serializer['permissions'] = [p['name'] for p in role_serializer['permissions']]
#    except:
#        user_serializer=None
#    
#    return user_serializer



@api_view(['GET'])
@is_authenticated
def authenticate_user(request,**kwargs):
    try:
        user_data = get_user(kwargs['user'])
        message='Success'
        status=200
    except:
        meassge='Something went Wrong!!'
        status=500
        
    return Response(
        {"user":user_data,"message":message},status=status
    )

@api_view(['GET'])
@is_authenticated
def get_user_orders(request,**kwargs):
    start = time.time()
    try:
        orders = Order.objects.filter(customer_id=kwargs['user'])
        data = get_orders_details(orders)

    except:
        return JsonResponse({
            'Error': 'Something went Wrong!!'
        },status=500)


    end=time.time()
    print(end-start)
    return JsonResponse({
            'Orders': data
    },status=200)



class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
#    permission_classes = [IsAuthenticated]
#    permission_object = 'roles'

    def list(self, request):
        try:
            role_serializer = RoleSerializer(Role.objects.all(), many=True).data
        except:
            role_serializer=None

        return Response({
            'Roles': role_serializer
        })

    def create(self, request):
        
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
            
        
        return Response({
            'role': serializer.data
        }, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(role)

        return Response({
            'role': serializer.data
        })


    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializer(instance=role, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'role': serializer.data
        }, status=status.HTTP_202_ACCEPTED)
    

    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        print(role)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


