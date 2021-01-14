from django.urls import path
from django.views import generic
from django.contrib.auth.decorators import login_required


from . import views
from . import forms
from .models import *
from .views import *

urlpatterns = [
    path('', views.index_productos, name='index_productos'),
    path('nuevo/', productos_view.as_view(), name='productos_view'),
    # path('nuevo/', productos_view.as_view(), name='productos_view'),
    # path('editar/<pk>', views.editar_producto, name='editar_producto'),
    path('editar_producto/<pk>', editar_producto.as_view(), name='editar_producto'),


    # path('nuevo/', login_required(crearProducto.as_view()), name='crearProducto'),
]