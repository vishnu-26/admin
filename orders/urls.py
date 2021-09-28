from django.urls import path,include
from django.conf.urls import url
from .views import (get_orders,
                    create_order,
                    create_order_item,
                    get_order,
                    export_orders_to_csv,
                    chart_api_view,
                    )

urlpatterns = [
    
    path('', get_orders , {'permission_object':'orders'}),
    path('create_order/', create_order , {'permission_object':'orders'}),
    path('create_order_item/', create_order_item , {'permission_object':'orders'}),
    url('get_order',get_order,{'permission_object':'orders'}),
    path('export/',export_orders_to_csv , {'permission_object':'orders'}),
    url(r'^chart_view/$', chart_api_view , {'permission_object':'orders'}),

]
