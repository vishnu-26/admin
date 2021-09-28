from django.urls import path,include
from . import views


app_name='frontend'
urlpatterns = [
    path('',views.login,name='login'),
    
]