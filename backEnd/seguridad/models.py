from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def upload_location(instance, filename):
    #Esta función guarda las imágenes de los usuarios en media_cdn/<id_usuario>
    return "usuarios/%s/%s" %(instance.username, filename)
    
class Usuario(AbstractUser):
    cedula = models.CharField(unique=True, max_length=10, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    sexo = models.TextField()
    area = models.TextField()
    cargo = models.TextField()
    estado = models.TextField()
    telefono = models.CharField(max_length=10)
    observaciones = models.TextField(blank=True)
    imagen = models.ImageField(upload_to=upload_location, blank=True, null=True)
    # fecha_nac = models.DateField(blank=True, null=True)
    # rol = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_privilegios(self):
        return RolPermisoUsuario.objects.filter(usuario=self.pk).values()

class RolPermisoUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.TextField()
    modulo = models.TextField()