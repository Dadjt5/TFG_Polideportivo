from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario import Usuario

class Monitor(Usuario):
    """Modelo para representar al monitor"""
    @classmethod
    def contar(cls):
        return cls.objects.count()