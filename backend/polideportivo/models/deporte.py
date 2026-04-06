from django.db import models
from django.utils.translation import gettext_lazy as _

class Deporte(models.Model):
    """Modelo para representar un deporte"""

    titulo = models.CharField(max_length=256, unique=True, blank=True)

    def __str__(self):
        return f'{self.titulo}'
    
    # Función para contar los deportes del sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()
