# blog/models.py
# Define los datos #

from django.db import models
from django.urls import reverse

# Create your models here.
# Determina qué se va a guardar en la base de datos
# Y cómo se va a mostrar en el panel de administración

class Post(models.Model):
    titulo      = models.CharField(max_length=200)
    anno        = models.PositiveIntegerField(blank=True, null=True, 
        help_text="Formato de 4 dígitos" )
    duracion    = models.PositiveIntegerField(blank=True, null=True,
        help_text="Minutos" )
    pais        = models.CharField(max_length=200, blank=True)
    direccion   = models.CharField(max_length=200, blank=True)
    guion       = models.TextField(default='', blank=True)
    reparto     = models.TextField(default='', blank=True)
    generos     = models.TextField(default='', blank=True)
    sinopsis    = models.TextField(default='', blank=True)
    fecha       = models.DateTimeField(auto_now_add=True) # Del sistema
    autor       = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    imagen = models.ImageField(upload_to='posts/', blank=True, null=True)
    # ImageField permite guardar imágenes asociadas a cada registro.
    # upload_to define la carpeta donde se almacenan las imágenes, estarían media/posts/

    def duracion_formateada(self):
        if self.duracion is not None:
            horas = self.duracion // 60
            minutos = self.duracion % 60
            return f"{horas}h {minutos}min"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("detalle_post", kwargs={"pk": self.pk})


    @property
    def campos_no_vacios(self):
        return {
            "Año": self.anno,
            "Duración": self.duracion_formateada(),
            "País": self.pais,
            "Dirección": self.direccion,
            "Guión": self.guion,
            "Reparto": self.reparto,
            "Géneros": self.generos,
            "Sinopsis": self.sinopsis,
        }.items()