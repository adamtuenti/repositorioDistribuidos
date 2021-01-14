from django.contrib import admin
from .models import SolicitudCompra, ProductoSolicitud

# Register your models here.

admin.site.register(SolicitudCompra)
admin.site.register(ProductoSolicitud)