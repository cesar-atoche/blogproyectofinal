from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fecha = models.DateField()
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    comentario = models.TextField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    fecha = models.DateField()
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)
