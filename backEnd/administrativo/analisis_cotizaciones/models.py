from django.db import models
from django.db.models import Model 
from datetime import datetime
from multiselectfield import MultiSelectField
from financiero.orden_pago.models import Centro_Costos
from administrativo.proveedores.models import Proveedor
from administrativo.solicitudes_compra.models import SolicitudCompra


class AnalisisCotizaciones(models.Model):
    ESTADO_CHOICES = [("Elaborado","Elaborado"), ("Aprobado","Aprobado"), ("Anulada","Anulada"),]
    PROCEDIMIENTO_SUGERIDO_CHOICES = [("Catálogo Electrónico","Catálogo Electrónico"), ("Subasta Inversa","Subasta Inversa"), ("Ínfima Cuantía","Ínfima Cuantía"),
    ("Menor Cuantía","Menor Cuantía"), ("Cotización","Cotización"), ("Licitación","Licitación"), ("Contratación Directa","Contratación Directa"),
     ("Contratación  integral por Precio Fijo","Contratación  integral por Precio Fijo"), ("Lista Corta","Lista Corta"), ("Concurso Público","Concurso Público"),]
    PERIODO_COMPRA_CHOICES = [("Diario","Diario"), ("Quincenal","Quincenal"), ("Mensual","Mensual"),
    ("Trimestral","Trimestral"), ("Cuatrimestral","Cuatrimestral"), ("Semestral","Semestral"),
    ("Anual","Anual"), ("No aplica","No aplica"),]
    TIPO_PROCESO_CHOICES = [("Bienes y Servicios Normalizados","Bienes y Servicios Normalizados"), ("Bienes y Servicios No Normalizados","Bienes y Servicios No Normalizados"),
    ("Obras","Obras"), ("Consultoría","Consultoría"),]
    TIPO_COMPRA_CHOICES = [("Bienes","Bienes"), ("Servicios","Servicios"),]
    TIPO_PROVEEDOR_CHOICES = [("Natural","Natural"), ("Jurídica","Jurídica"),]

    fecha = models.DateField(default=datetime.now, blank=True)
    tipo_proceso = models.CharField(max_length=50, verbose_name="Tipo de Proceso",blank=True, null=True, choices=TIPO_PROCESO_CHOICES)
    tipo_proveedor = models.CharField(max_length=50, verbose_name="Tipo de Proveedor",blank=True, null=True, choices=TIPO_PROVEEDOR_CHOICES)
    procedimiento_sugerido = models.CharField(max_length=50, verbose_name="Procedimiento sugerido",blank=True, null=True, choices=PROCEDIMIENTO_SUGERIDO_CHOICES)
    tipo_compra = models.CharField(max_length=50, verbose_name="Tipo de Compra",blank=True, null=True, choices=TIPO_COMPRA_CHOICES)
    centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    estado = models.CharField(max_length=50, verbose_name="Estado",blank=True, null=True, choices=ESTADO_CHOICES)
    fecha_aprobacion = models.DateField(default=datetime.now, blank=True)
    detalle_proceso = models.CharField(max_length=500, verbose_name="Detalle del proceso", blank=True, null=True)
    ruc = models.CharField(max_length=500, verbose_name="RUC", blank=False, null=True)
    razon = models.CharField(max_length=500, verbose_name="Razón Social", blank=False, null=True)
    criterio_seleccion = models.CharField(max_length=500, verbose_name="Criterio de Selección", blank=True, null=True)
    valor_letras = models.CharField(max_length=500, verbose_name="Son valor en letras", blank=True, null=True)
    

    cod_analisis = models.CharField(max_length=20, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL,null=True)
    cod_solicitud = models.ForeignKey(SolicitudCompra, on_delete=models.SET_NULL,null=True)
     

    def __str__(self):
        return self.cod_analisis

