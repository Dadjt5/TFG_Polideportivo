from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.conf import settings

from .usuario_final import UsuarioFinal

class Foro(models.Model):
    """Modelo para representar el foro"""

    titulo = models.CharField(max_length=256)
    numeroParticipantes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Foro con {self.numeroParticipantes}'

    def nuevoCanal(self, titulo, tema, secreto, oculto):
        try:
            with transaction.atomic():
                canal = Canal.objects.create(titulo=titulo, tema=tema, secreto=secreto, oculto=oculto, foro=self, numeroParticipantes=0)

                for usuario in UsuarioFinal.objects.all():
                    canal.añadirUsuario(usuario)

            return True
        except Exception:
            return False


class UsuarioCanal(models.Model):
    """Modelo para representar la relación entre canal y usuario"""

    fechaEntrada = models.DateField(auto_now=True)
    silenciado = models.BooleanField(default=False)
    expulsado = models.BooleanField(default=False)
    
    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT, related_name="canales")
    canal = models.ForeignKey('Canal', on_delete=models.CASCADE, related_name="usuarioFinal")

    class Meta:
        unique_together = ('usuarioFinal', 'canal')
    

class Canal(models.Model):
    """Modelo para representar un canal"""

    titulo = models.CharField(max_length=256)
    tema = models.CharField(max_length=256)
    numeroParticipantes = models.PositiveIntegerField(default=0)
    oculto = models.BooleanField(default=False)
    secreto = models.BooleanField(default=False)

    foro = models.ForeignKey(Foro, on_delete=models.RESTRICT, related_name="canal")

    def __str__(self):
        return f'Canal para {self.titulo} con {self.numeroParticipantes} participantes'
    
    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    def getMensajes(self):
        return self.mensajes.all()
    
    def nuevoMensaje(self, usuario, texto):
        if not usuario:
            return False
        
        if usuario.is_administrador:
            Mensaje.objects.create(canal=self, usuario=usuario, texto=texto)
            return True

        relacion = UsuarioCanal.objects.filter(
            usuarioFinal=usuario.usuario_final,
            canal=self,
            expulsado=False,
            silenciado=False
        ).first()

        if not relacion:
            return False

        Mensaje.objects.create(canal=self, usuario=usuario, texto=texto)
        return True

    def cambiarExpulsionUsuario(self, usuarioFinal):
        try:
            relacion = UsuarioCanal.objects.get(usuarioFinal=usuarioFinal, canal=self)
        except:
            return False

        with transaction.atomic():
            relacion.expulsado = not relacion.expulsado
            relacion.save(update_fields=["expulsado"])

            if relacion.expulsado:
                self.numeroParticipantes -= 1
            else:
                self.numeroParticipantes += 1
            self.save(update_fields=["numeroParticipantes"])

        return True

    def añadirUsuario(self, usuarioFinal):
        with transaction.atomic():
            relacion, creada = UsuarioCanal.objects.get_or_create(
                usuarioFinal=usuarioFinal,
                canal=self
            )

            if not creada:
                return False

            self.numeroParticipantes += 1
            self.foro.numeroParticipantes += 1

            self.save(update_fields=["numeroParticipantes"])
            self.foro.save(update_fields=["numeroParticipantes"])

        return True

    def cambiarSilencioUsuario(self, usuarioFinal):
        try:
            relacion = UsuarioCanal.objects.get(usuarioFinal=usuarioFinal, canal=self)
            relacion.silenciado = not relacion.silenciado
            relacion.save(update_fields=["silenciado"])
            return True
        except:
            return False


class Mensaje(models.Model):
    """Mensaje enviado en un canal del foro"""

    texto = models.TextField()
    fechaEnvio = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    canal = models.ForeignKey('Canal', on_delete=models.CASCADE, related_name="mensajes")

    class Meta:
        ordering = ["fechaEnvio"]

    def __str__(self):
        return f"Mensaje en {self.canal.titulo}"