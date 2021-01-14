from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Bien)
admin.site.register(Ingreso_Bien)
admin.site.register(Detalle_Ingreso_Bien)