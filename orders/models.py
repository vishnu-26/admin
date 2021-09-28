from django.db import models
from user.models import User
from products.models import Product
#from .serializers import OrderSerializer,OrderItemSerializer

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

#    def save(self,*args,**kwargs):
#        super(Order,self).save(*args,**kwargs)

    

     


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    
