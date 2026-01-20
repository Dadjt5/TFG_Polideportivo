from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorito(models.Model):
    """Modelo para representar las instalaciones y actividades marcadas como favoritas por un usuario final"""

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT, related_name="favoritos")
    actividad = models.ForeignKey('Actividad', on_delete=models.RESTRICT, null=True)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT, null=True)
    
    @classmethod
    def contar(cls):
        return cls.objects.count()

    class Meta:
        unique_together = ('usuarioFinal', 'actividad', 'instalacion')
        
    def __str__(self):
        if self.actividad:
            return f"{self.usuarioFinal} tiene como actividad favorita: {self.actividad}"
        elif self.instalacion:
            return f"{self.usuarioFinal} tiene como instalación favorita: {self.instalacion}"
        return f"{self.usuarioFinal} sin favoritos"
