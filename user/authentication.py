import jwt
import datetime
from django.conf import settings
from .models import User
from rest_framework.authentication import BaseAuthentication
from django.http import JsonResponse,HttpResponse

def generate_token(user):
    payload={
        'user_id':user.user_id,
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#        'jwt':datetime.datetime.utcnow()
    }

    return jwt.encode(payload,settings.SECRET_KEY,'HS256')


#This is used for function based views
def is_authenticated(function):
    
    def wrapper(request,**kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]

            if not token:
                return JsonResponse({
                   'Error' : 'Unauthenticated user!!',
                },status=401)
            
            payload=jwt.decode(token,settings.SECRET_KEY,'HS256')
            user = User.objects.filter(user_id=payload['user_id']).first()
        except:
            return JsonResponse({
                   'Error' : 'Unauthenticated user!!',
            },status=401)
        
        kwargs['user']=user
#        print(kwargs) 
        return function(request,**kwargs)

    return wrapper
        



#This is used for class based views
class JWTAuthentication(BaseAuthentication):

    def authenticate(self,function):

        try:
            token = request.META.get('HTTP_AUTHORIZATION').split()[1]

            if not token:
                return None
            
            payload=jwt.decode(token,settings.SECRET_KEY,'HS256')
            user = User.objects.filter(user_id=payload['user_id']).first()
        except:
#            print("hii")
            return None
        
        
#        print(user)
        return (user,token)


        

    
