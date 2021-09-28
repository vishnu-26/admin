from django.urls import path,include
from .views import authenticate_user,register,login,RoleViewSet,get_user_orders


app_name='user'
urlpatterns = [
#    path('getusers',users,name='users'),
    path('register/',register),
    path('login/',login),
    path('getuser/',authenticate_user),
    path('orders/',get_user_orders),
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('role/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]
