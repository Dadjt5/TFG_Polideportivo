from django.db import models
from django.utils.translation import gettext_lazy as _

class Deporte(models.Model):
    """Modelo para representar los deportes"""

    titulo = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.titulo}'
