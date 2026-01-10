from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .usuario import Usuario

class Monitor(Usuario):
    """Modelo para representar al monitor"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="monitor")

    @classmethod
    def contar(cls):
        return cls.objects.count()