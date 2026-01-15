from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password

from .usuario_final import UsuarioFinal


class TDA(models.Model):
    """Modelo para representar una actividad"""

    fechaInicio = models.DateField(auto_now_add=True)
    fechaExpiracion = models.DateField()
    _codigo_secreto_hash = models.CharField(max_length=128, blank=True)
    
    usuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.RESTRICT, related_name="tda", blank=True, null=True)

    def __str__(self):
        return f'Tarjeta deportiva anual con fecha de inicio: {self.fechaInicio} y fecha de expiracion: {self.fechaExpiracion}'

    def nuevo_codigo_secreto(self, codigo: str):
        self._codigo_secreto_hash = make_password(codigo)

    def comprobar_codigo_secreto(self, codigo: str) -> bool:
        return check_password(codigo, self._codigo_secreto_hash)

    def asignar_usuario(self, usuario_final):
        if self.usuarioFinal:
            return False

        self.usuarioFinal = usuario_final
        self.save()

        return True

    @classmethod
    def contar(cls):
        return cls.objects.count()