from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario import Usuario
from .deporte import Deporte
from .foro import Canal
from .constantes import Sexo, Rol

class UsuarioFinal(models.Model):
    """Modelo para representar al usuario final"""
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="usuario final")
    
    fechaNacimiento = models.DateField(auto_now_add=True)
    telefono = models.CharField(default=16)
    provincia = models.CharField(default=64)
    municipio = models.CharField(default=64)
    localidad = models.CharField(default=64)
    codigoPostal = models.CharField(default=64)
    cuentaBancaria = models.CharField(default=64)
    solicitaCreditos = models.CharField(default=False)
    actividadesRealizadas = models.IntegerField(default=0)
    
    deportesFavoritos = models.ManyToManyField(Deporte, blank=True, related_name="usuarios")
    canales = models.ManyToManyField(Canal, blank=True, related_name="usuarios")

    sexo = models.CharField(default=Sexo.NINGUNO, choices=Sexo.choices)
    rol = models.CharField(default=Rol.EXTERNO, choices=Rol.choices)
    
    def __str__(self):
        return f'{self.usuario}'
