from django.db import models
from django.db.models import Model
from datetime import datetime
from multiselectfield import MultiSelectField
from administrativo.proveedores.models import Proveedor
from financiero.orden_pago.models import Centro_Costos
from administrativo.productos.models import Producto

class Bien(models.Model):
    TIPO_BIEN_CHOICES=[("Activo","Activo"), ("Bien Sujeto a control administrativo","Bien Sujeto a control administrativo"),]
    CATEGORIA_CHOICES=[("Categoria1","Categoria1"), ("Categoria2","Categoria2"),]
    ESTADO_CHOICES = [("Activo","Activo"), ("Inactivo","Inactivo"),]
    MANTENIMIENTO_CHOICES= [("Diario","Diario"), ("Quincenal","Quincenal"),("Mensual","Mensual"),("Trimestral","Trimestral"),("Cuatrimestral","Cuatrimestral"),("Quimestral","Quimestral"),("Semestral","Semestral"),("Anual","Anual"),("No Aplica","No Aplica")]
    TIPO_MANTENIMIENTO_CHOICES= [("Preventivo","Preventivo"), ("Correctivo","Correctivo"),]
    STATE_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
    )

    cod_activo = models.CharField(max_length=20, blank=True)
    cod_bien = models.CharField(max_length=20, blank=True)
    fecha = models.DateField(default=datetime.now, blank=True)
    fecha_registro = models.DateField(default=datetime.now, blank=True)
    nombre = models.CharField(max_length=20, blank=True)
    marca = models.CharField(max_length=20, blank=True)
    modelo = models.CharField(max_length=20, blank=True)
    n_serie = models.CharField(max_length=20, blank=True)
    tipo_bien = models.CharField(max_length=50, verbose_name="Tipo de Bien",blank=True, null=True, choices=TIPO_BIEN_CHOICES)
    categoria = models.CharField(max_length=50, verbose_name="categoria",blank=True, null=True, choices=CATEGORIA_CHOICES)
    estado = models.CharField(max_length=50, verbose_name="Estado",blank=True, null=True, choices=ESTADO_CHOICES)
    inventario = models.BooleanField('Inventario', default= False, blank=True, null=True, choices=STATE_CHOICES)
    iva = models.BooleanField('IVA', default= False, blank=True, null=True, choices=STATE_CHOICES)
    cod_inventariound = models.CharField(max_length=20, blank=True)
    cod_Espoltech = models.CharField(max_length=20, blank=True)
    fecha_compra = models.DateField(default=datetime.now, blank=True)
    frecuencia_mantenimiento = models.CharField(max_length=50, verbose_name="Mantenimiento",blank=True, null=True, choices=MANTENIMIENTO_CHOICES)
    tipo_mantenimiento = models.CharField(max_length=50, verbose_name="Tipo de Mantenimiento",blank=True, null=True, choices=TIPO_MANTENIMIENTO_CHOICES)
    caracteristicas = models.CharField(max_length=500,blank=True, null=True)
    subtotal = models.FloatField(default=0)
    valor_iva = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    observaciones = models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)
    fecha_inventario = models.DateField(default=datetime.now, blank=True)
    ubicacion_inicial = models.CharField(max_length=50, blank=True)
    ubicacion_final = models.CharField(max_length=50, blank=True)
    centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL,null=True)
    fecha_facturacion=models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.cod_bien


class Ingreso_Bien(models.Model):
    cod_orden = models.CharField(max_length=20, blank=True)
    fecha_Registro = models.DateField(default=datetime.now, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=False, null=True)
    ruc_proveedor = models.CharField(max_length=20, blank=False)
    num_factura = models.CharField(max_length=20, blank=False)
    fecha_factura = models.DateField(default=datetime.now, blank=True)
    centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    observaciones = models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)
    subtotal = models.FloatField(default=0)
    valor_iva = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return self.cod_orden   

class Detalle_Ingreso_Bien(models.Model):
    ingreso_bien = models.ForeignKey(Ingreso_Bien, on_delete=models.SET_NULL, null=True)
    fecha_Registro = models.DateField(default=datetime.now, blank=True)
    bien = models.ForeignKey(Bien, on_delete=models.SET_NULL, null=True)
    cantidad = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    valor_iva = models.FloatField(default=0)
    total = models.FloatField(default=0)