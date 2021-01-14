from django.db import models
from ventas.personas_juridicas.models import Juridica, TipoEmpresa, Sector

# Create your models here.
class Proforma(models.Model):
	codigo=models.CharField(max_length=20, blank=True)
	version=models.PositiveIntegerField()
	tipoEmpresa=models.ForeignKey(TipoEmpresa, on_delete=models.CASCADE,null=True,blank=True)
	TIPO_CHOICES=[('Natural','Natural'),('Jurídica','Jurídica'),]
	
	tipo_cliente=models.CharField(max_length=15, choices=TIPO_CHOICES)
	ruc_ci=models.CharField(max_length=13)
    
	#empresa=models.ForeignKey(Juridica, on_delete=models.CASCADE,verbose_name="")

	asesor=models.CharField(max_length=50)
	
	razon_nombres=models.CharField(max_length=200)

	sector=models.ForeignKey(Sector, on_delete=models.CASCADE,null=True,blank=True)
	fechaSolicitud=models.DateField()
	fechaEnvio=models.DateField()
	numeroParticipantes=models.PositiveIntegerField()
	horas=models.PositiveIntegerField()
	cantidadCursos=models.PositiveIntegerField()
	estado=models.CharField(max_length=30,verbose_name="")
	porcentExito=models.FloatField()
	porcentDesc=models.FloatField(blank=True, null=True)
	montoProforma=models.FloatField()
	montoDesc=models.FloatField(blank=True, null=True)
	observacion=models.CharField(max_length=500,blank=True, null=True)
	fechaRespuesta=models.DateField(blank=True, null=True)
	montoAceptado=models.FloatField(blank=True,null=True)
	montoEjecutado=models.FloatField(blank=True,null=True)
	montoPorEjecutarse=models.FloatField(blank=True,null=True)
	active=models.BooleanField(default = True)


class ProformaFile(models.Model):
    file = models.FileField(upload_to='uploads/',blank=True, null=True)
    #file = models.CharField(max_length=50, blank=True,default=" ")
    #propuesta = models.ManyToManyField(PropuestaCorporativo, through='PropFileKey')
    proforma=models.ForeignKey(Proforma, on_delete=models.CASCADE)
	