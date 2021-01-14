from django.contrib import admin
from financiero.orden_facturacion.models import OrdenFacturacion,OrdenFacturacionParticipante

# Register your models here.
admin.site.register(OrdenFacturacion)
admin.site.register(OrdenFacturacionParticipante)