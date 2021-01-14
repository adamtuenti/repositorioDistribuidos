from django.contrib import admin
from .models import Seguimiento_Interesados
from .models import Seguimiento_PersonaNatural,SeguimientoEmpresa
# Register your models here.
admin.site.register(Seguimiento_Interesados)
admin.site.register(Seguimiento_PersonaNatural)
admin.site.register(SeguimientoEmpresa)