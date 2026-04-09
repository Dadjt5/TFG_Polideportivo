from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, UniqueConstraint


class Favorito(models.Model):
    """Modelo para representar las instalaciones y actividades marcadas como favoritas por un usuario final"""

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE, related_name="favoritos")
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, null=True)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE, null=True)
    
    # Función para contar el número de favoritos
    @classmethod
    def contar(cls):
        return cls.objects.count()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['usuarioFinal', 'actividad'],
                condition=Q(actividad__isnull=False),
                name='unique_usuario_actividad'
            ),

            UniqueConstraint(
                fields=['usuarioFinal', 'instalacion'],
                condition=Q(instalacion__isnull=False),
                name='unique_usuario_instalacion'
            )
        ]
        
    def __str__(self):
        if self.actividad:
            return f"{self.usuarioFinal} tiene como actividad favorita: {self.actividad}"
        elif self.instalacion:
            return f"{self.usuarioFinal} tiene como instalación favorita: {self.instalacion}"
        return f"{self.usuarioFinal} sin favoritos"
