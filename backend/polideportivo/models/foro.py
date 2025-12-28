from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario_final import UsuarioFinal
from .constantes import Tematica


class Foro(models.Model):
    """Modelo para representar el foro"""

    numeroParticipantes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Foro con {self.numeroParticipantes}'

    def nuevoCanal(self, titulo: str):
        try:
            canal = Canal.objects.create(titulo=titulo, foro=self, numeroParticipantes=0)
            
            for usuario in UsuarioFinal.objects.all():
                UsuarioCanal.objects.get_or_create(usuarioFinal=usuario, canal=canal)
            return True
        except Exception:
            return False


class UsuarioCanal(models.Model):
    """Modelo para representar la relación entre canal y usuario"""

    fechaEntrada = models.DateField(auto_now=True)
    silenciado = models.BooleanField(default=False)
    expulsado = models.BooleanField(default=False)
    
    usuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.RESTRICT)
    canal = models.ForeignKey('Canal', on_delete=models.RESTRICT)
    
    class Meta:
        unique_together = ('usuarioFinal', 'canal')
    

class Canal(models.Model):
    """Modelo para representar un canal"""

    titulo = models.CharField(max_length=256, blank=True)
    numeroParticipantes = models.PositiveIntegerField(default=1)
    oculto = models.BooleanField(default=False)
    secreto = models.BooleanField(default=False)

    foro = models.ForeignKey(Foro, on_delete=models.RESTRICT)

    tema = models.CharField(default=Tematica.CHAT, choices=Tematica.choices)

    def __str__(self):
        return f'Canal para {self.titulo} con {self.numeroParticipantes} participantes'
    
    @classmethod
    def contar(cls):
        return cls.objects.count()

    def expulsarUsuario(self, usuarioFinal):
        try:
            relacion = UsuarioCanal.objects.get(usuarioFinal=usuarioFinal, canal=self)
            if relacion.expulsado == False:
                return False
            
            relacion.expulsado = True
            relacion.save(update_fields=["expulsado"])
            return True
        except:
            return False

    def añadirUsuario(self, usuarioFinal):
        UsuarioCanal.objects.get_or_create(usuarioFinal=usuarioFinal, canal=self)

    def cambiarSilencioUsuario(self, usuarioFinal):
        try:
            relacion = UsuarioCanal.objects.get(usuarioFinal=usuarioFinal, canal=self)
            relacion.silenciado = not relacion.silenciado
            relacion.save(update_fields=["silenciado"])
            return True
        except:
            return False
