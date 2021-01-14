from django.db import models
from django.db.models import Model
from datetime import datetime
from multiselectfield import MultiSelectField
from administrativo.proveedores.models import Proveedor
from financiero.orden_pago.models import Centro_Costos
from administrativo.productos.models import Producto

class Suministro(models.Model):
    
    PROVEEDORES_CHOICES = [("Natural", "Natural"),("Jurídica", "Jurídica"),]

    cod_suministro=models.CharField(max_length=20, blank=True)
    fecha=models.DateField(default=datetime.now, blank=True)
    tipo_proveedor = models.CharField(max_length=10, choices=PROVEEDORES_CHOICES, blank=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL,null=True)
    numero_factura=models.PositiveIntegerField()
    fecha_facturacion=models.DateField(default=datetime.now, blank=True)
    centro_costos=models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    observaciones=models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)
    subtotal=models.FloatField(default=0)
    valor_iva=models.FloatField(default=0)
    total=models.FloatField(default=0)
    
    def __str__(self):
        return self.cod_suministro    


class ProductoSuministro(models.Model):
    suministro=models.ForeignKey(Suministro, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad=models.FloatField(default=0)
    precio=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    subtotal=models.FloatField(default=0)


