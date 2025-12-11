from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario import Usuario

class Monitor(models.Model):
    """Modelo para representar al monitor"""

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="monitor")

    def __str__(self):
        return f'{self.usuario}'