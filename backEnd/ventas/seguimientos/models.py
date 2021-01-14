from django.db import models
from ..personas_juridicas.models import Juridica
from ..reporte_contacto.models import ReporteContacto
from ..interesados.models import CanalContacto
from academico.evento.models import Evento
from ventas.personas_naturales.models import Persona_Natural
from ventas.interesados.models import Interesado,CanalContacto
from educacion_continua import settings
from seguridad.models import Usuario

# Create your models here.

TIPO_CHOICES = [  
        ('NATURAL','Natural'),
        ('INTERESADO','Interesado'),
    ]
ESTADO_CHOICES = [  
        ('PCTC','Por contactar'),
        ('SNRP','Sin respuesta'),
        ('CTDO','Contactado'),
        ('INVD','Contacto inválido'),
    ]
EXITO_CHOICES = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    ]
INSCRIPCION_CHOICES = [
        ('AUFN','Autofinanciada'),
        ('ASPD','Auspiciada'),
        ('MXTA','Mixta'),
    ]

class Seguimiento_PersonaNatural(models.Model):
    ESTADO_CHOICES = [  
        ('PCTC','Por contactar'),
        ('SNRP','Sin respuesta'),
        ('CTDO','Contactado'),
        ('INVD','Contacto inválido'),
    ]
    EXITO_CHOICES = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    ]
    INSCRIPCION_CHOICES = [
        ('AUFN','Autofinanciada'),
        ('ASPD','Auspiciada'),
        ('MXTA','Mixta'),
    ]
    ESTADO_PARTICIPANTE_CHOICES = [
        ('INSC','Inscrito'),
        ('PGTO','Pre-registrado'),
        ('EGTO','En seguimiento'),
        ('NIDO','No interesado'),
        ('DVCN','Devolución'),
        ('CMTO','Cambio evento'),
        ('CPTE','Cambio participante')
    ]
    n_registro = models.CharField(max_length=7,blank= True)
    fecha_registro = models.DateField()
    fecha_seguimiento = models.DateField()
    estado_seguimiento = models.CharField(max_length=5, choices = ESTADO_CHOICES)
    canal_de_contacto = models.ForeignKey(CanalContacto, on_delete=models.SET_NULL, blank=False, null=True)
    exito = models.IntegerField(choices= EXITO_CHOICES)
    proximo_seguimiento = models.DateField(blank = True, null = True)
    cod_evento=models.CharField(max_length=20)
    nombre_evento=models.CharField(max_length=500)
    tipo_inscripcion = models.CharField(max_length = 5 , choices =INSCRIPCION_CHOICES,  null = True )
    observaciones = models.TextField(max_length=850,blank = True, null = True)
    pers_natural = models.ForeignKey(Persona_Natural, blank = True, null = True, on_delete=models.CASCADE)

    # fecha_porcontactar=models.DateField(blank = True, null = True)
    # fecha_sinrespuesta=models.DateField(blank = True, null = True)
    # fecha_contactado=models.DateField(blank = True, null = True)
    # fecha_contactoinvalido=models.DateField(blank = True, null = True)
    #asesor=models.CharField(max_length = 400,blank = True, null = True)
    asesor=models.ForeignKey(Usuario, blank = True, null = True, on_delete=models.CASCADE)
    estado_participante = models.CharField(max_length = 5 , choices =ESTADO_PARTICIPANTE_CHOICES )

    def __str__(self):
        return self.n_registro
    
class Seguimiento_Interesados(models.Model):
    n_registro_interesado = models.CharField(max_length=7,blank= True)
    fecha_registro = models.DateField()
    fecha_seguimiento = models.DateField()
    estado_seguimiento = models.CharField(max_length=5, choices = Seguimiento_PersonaNatural.ESTADO_CHOICES)
    canal_de_contacto = models.ForeignKey(CanalContacto, on_delete=models.SET_NULL, blank=False, null=True)
    exito = models.IntegerField(choices= Seguimiento_PersonaNatural.EXITO_CHOICES)
    proximo_seguimiento = models.DateField(blank = True, null = True)
    cod_evento=models.CharField(max_length=20)
    nombre_evento=models.CharField(max_length=500)
    observaciones = models.TextField(max_length=850,blank = True, null = True)
    inters= models.ForeignKey(Interesado,blank=True,null=True, on_delete=models.CASCADE)

    # fecha_porcontactar=models.DateField(blank = True, null = True)
    # fecha_sinrespuesta=models.DateField(blank = True, null = True)
    # fecha_contactado=models.DateField(blank = True, null = True)
    # fecha_contactoinvalido=models.DateField(blank = True, null = True)
    asesor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)
    estado_participante = models.CharField(max_length = 5 , choices =Seguimiento_PersonaNatural.ESTADO_PARTICIPANTE_CHOICES )
    
    def __str__(self):
        return self.n_registro_interesado

    
# Create your models here.

class EstadoSeguimiento(models.Model):
    nombre=models.CharField(max_length=25)

    def __str__(self):
        return self.nombre


TIPO_EVENTO=[('Abierto','Abierto'),('Corporativo','Corporativo')]
TIPO_OFERTA=[('Propuesta','Propuesta'),('Proforma','Proforma'),('Directa','Directa')]
EXITO_CHOICES=[(1,1),(2,2),(3,3),(4,4),(5,5)]

class SeguimientoEmpresa(models.Model):
    juridica=models.ForeignKey(Juridica,on_delete=models.CASCADE)
    n_seguimiento=models.CharField(max_length=20, verbose_name="N° de Registro",blank=True)
    fecha=models.DateField(verbose_name='Fecha Registro')
    fecha_seguimiento=models.DateField(verbose_name='Fecha Seguimiento')
    estado=models.ForeignKey(EstadoSeguimiento,on_delete=models.SET_NULL,null=True,default=1,verbose_name='Estado de Seguimiento')
    canal=models.ForeignKey(CanalContacto,on_delete=models.SET_NULL,null=True,default=6,verbose_name='Canal de Contacto')
    exito=models.IntegerField(choices=EXITO_CHOICES,verbose_name='Éxito')
    tipo_evento=models.CharField(max_length=20,choices=TIPO_EVENTO,verbose_name='Tipo de Evento')
    tipo_oferta=models.CharField(max_length=20,choices=TIPO_OFERTA,verbose_name='Tipo de Oferta')
    n_oferta=models.CharField(max_length=50,verbose_name='N° de Oferta',blank=True)
    reporte_contacto=models.ForeignKey(ReporteContacto,null=True,on_delete=models.SET_NULL,verbose_name="Reporte de contacto")
    n_participantes=models.PositiveIntegerField(verbose_name="N° de Participantes")
    fecha_proximo=models.DateField(verbose_name='Próximo seguimiento',null=True,blank=True)
    fecha_por_contactar=models.DateField(null=True,blank=True)
    fecha_sin_respuesta=models.DateField(null=True,blank=True)
    fecha_contactado=models.DateField(null=True,blank=True)
    fecha_contacto_invalido=models.DateField(null=True,blank=True)
    observaciones=models.CharField(verbose_name='Observaciones',blank=True, max_length=500)
    n_evento=models.IntegerField(default=0)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)
    
class SeguimientoEmpresaEventos(models.Model):
    seguimiento_empresa=models.ForeignKey(SeguimientoEmpresa,on_delete=models.CASCADE)
    evento=models.ForeignKey(Evento,on_delete=models.CASCADE)
    nombre_evento=models.CharField(max_length=100)
    codigo_evento=models.CharField(max_length=50)