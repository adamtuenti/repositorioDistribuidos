from django.db import models
from django.db.models import Model 
from datetime import datetime
from multiselectfield import MultiSelectField

class Producto(models.Model):
    TIPO_PRODUCTO_CHOICES = [("Bienes","Bienes"), ("Servicios","Servicios"),]
    UNIDAD_MEDIDA_CHOICES = [("Unidad","Unidad"), ("Caja","Caja"), ("Caneca","Caneca"), ("Resma","Resma"), ("Paquete","Paquete"), ("Galón","Galón"), ("Litro","Litro"), ("Otros","Otros"),]
    ESTADO_CHOICES = [("Activo","Activo"), ("Inactivo","Inactivo"),]
    CONTROLABLE_CHOICES = [("SI","SI"), ("NO","NO"),]
    STATE_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
    )

    cod_producto=models.CharField(max_length=20, blank=True)
    nombre=models.CharField(max_length=100)
    fecha=models.DateField(default=datetime.now, blank=True)
    tipo=models.CharField(max_length=50, verbose_name="Tipo de Producto",blank=True, null=True, choices=TIPO_PRODUCTO_CHOICES)
    unidad_medida=models.CharField(max_length=50, verbose_name="Unidad de Medida",blank=True, null=True, choices=UNIDAD_MEDIDA_CHOICES)
    estado=models.CharField(max_length=50, verbose_name="Estado",blank=True, null=True, choices=ESTADO_CHOICES)
    dias_entrega=models.PositiveIntegerField()
    
    # controlable=models.BooleanField('Controlable', default= False, blank=True, null=True)
    controlable=models.BooleanField('Controlable', default= False, blank=True, null=True, choices=STATE_CHOICES)

    # iva=models.BooleanField('IVA', default= False, blank=True, null=True)
    iva=models.BooleanField('IVA', default= False, blank=True, null=True, choices=STATE_CHOICES)

    punto_reorden=models.PositiveIntegerField()
    tolerancia=models.PositiveIntegerField()
    cant_maxima=models.PositiveIntegerField()
    stock_actual=models.IntegerField(default=0)
    descripcion=models.CharField(max_length=500,blank=True, null=True)



