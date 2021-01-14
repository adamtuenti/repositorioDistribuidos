from django.contrib import admin

# Register your models here.

from .models import Proveedor, TipoEmpresa

admin.site.register(Proveedor)
admin.site.register(TipoEmpresa)