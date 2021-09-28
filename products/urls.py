from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import get_products,upload_product

app_name='products'

urlpatterns = [

    path('',get_products),
    path('upload',upload_product),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
