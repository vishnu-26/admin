#import user.views
from orders.utils import get_order_detail
from .utils import get_user
from rest_framework import permissions
from .authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework.response import Response



class IsAuthenticated(permissions.BasePermission):
    
    def has_permission(self,request,view):
        auth = JWTAuthentication()
        
        if auth.authenticate(request):
            return True
        else:
            return False



class ViewPermission(permissions.BasePermission):

    def permission(self,request,view):
        pass



#kwargs['user'] is the user object
#user_detail is custom user data
def has_permission(function):
    def wrapper(request,**kwargs):
#        print(kwargs)
        user_detail = get_user(kwargs['user'])
       
        

        if request.method == 'GET':
            view_access = any(p == 'view_' + kwargs['permission_object'] for p in user_detail['permissions'])

            if not view_access:
                try:
                    ##order_id when quering for particular order_id
                    print("hii")
                    order_id = request.query_params['order_id']
#                    print(get_order_detail(order_id)['customer_id'])
#                    print(kwargs['user'])
                    if get_order_detail(order_id)['customer_id'] == kwargs['user']:
                        raise Exception
                except Exception as e:
                    return Response({
                        'Error': 'You dont have permission to access this service!!'
                    },status=403)

            return function(request,**kwargs)


    return wrapper





