from django.db import models
import administrativo.validaciones
from datetime import datetime
from administrativo.proveedores.models import Proveedor
from administrativo.proveedores.models import TipoRubro
from academico.evento.models import Evento

#MODELO DE CALIFICACION DE PROVEEDORES

class Calificacion_proveedor(models.Model):

    PROVEEDORES_CHOICES = [("Natural", "Natural"),("Jurídica", "Jurídica"),]

    cod_calificacion=models.CharField(max_length=20, blank=True)
    fecha=models.DateField(default=datetime.now, blank=True)

    tipo_proveedor = models.CharField(max_length=10, choices=PROVEEDORES_CHOICES, blank=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL,null=True)
    evento=models.ForeignKey(Evento,on_delete=models.SET_NULL,null=True,blank=True)

    
    tipo_rubro=models.ForeignKey(TipoRubro, on_delete=models.CASCADE,null=True,blank=True)
    responsable=models.CharField(max_length=30,blank=True)
    cargo=models.CharField(max_length=30,blank=True)
    orden_compra=models.CharField(max_length=30, blank=True, null=True)
    numero_orden=models.CharField(max_length=30, blank=True, null=True)

    treinta=models.IntegerField(default=30, blank=True, null=True)
    veinticinco=models.IntegerField(default=25, blank=True, null=True)
    veinte=models.IntegerField(default=20, blank=True, null=True)
    quince=models.IntegerField(default=15, blank=True, null=True)
    diez=models.IntegerField(default=10, blank=True, null=True)
    cinco=models.IntegerField(default=5, blank=True, null=True)
    cero=models.IntegerField(default=0, blank=True, null=True)


    #Calidad del producto y/o servicio que presta
    determ_prod=models.IntegerField(default=25, blank=True, null=True)
    total_prod=models.IntegerField(default=0, blank=True, null=True)

    #Tiempos de entrega

    determ_tiempo=models.IntegerField(default=25, blank=True, null=True)
    total_tiempo=models.IntegerField(default=0, blank=True, null=True)


    #Tiempo de entrega del pedido

    determ_tiempopedido=models.IntegerField(default=30, blank=True, null=True)
    total_tiempopedido=models.IntegerField(default=0, blank=True, null=True)


    #Servicio al cliente
    determ_servicio=models.IntegerField(default=20, blank=True, null=True)
    total_servicio=models.IntegerField(default=0, blank=True, null=True)


    #
    descripcion=models.CharField(max_length=500, verbose_name="Descripcion", blank=True, null=True)

    #total calificaciones
    subtotal=models.IntegerField(default=100, blank=True, null=True)
    total=models.IntegerField(default=0, blank=True, null=True)


    #total otorgado por los portacipantes
    subtotal_participante=models.IntegerField(default=100, blank=True, null=True)
    total_participante=models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.cod_calificacion






